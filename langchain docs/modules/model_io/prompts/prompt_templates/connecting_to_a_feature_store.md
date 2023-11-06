# Connecting to a Feature Store

Feature stores are a concept from traditional machine learning that make sure data fed into models is up-to-date and relevant. For more on this, see [here](https://www.tecton.ai/blog/what-is-a-feature-store/).

This concept is extremely relevant when considering putting LLM applications in production. In order to personalize LLM applications, you may want to combine LLMs with up-to-date information about particular users. Feature stores can be a great way to keep that data fresh, and LangChain provides an easy way to combine that data with LLMs.

In this notebook we will show how to connect prompt templates to feature stores. The basic idea is to call a feature store from inside a prompt template to retrieve values that are then formatted into the prompt.

## Feast[​](#feast "Direct link to Feast")

To start, we will use the popular open-source feature store framework [Feast](https://github.com/feast-dev/feast).

This assumes you have already run the steps in the README around getting started. We will build off of that example in getting started, and create and LLMChain to write a note to a specific driver regarding their up-to-date statistics.

### Load Feast Store[​](#load-feast-store "Direct link to Load Feast Store")

Again, this should be set up according to the instructions in the Feast README.

```python
from feast import FeatureStore  
  
# You may need to update the path depending on where you stored it  
feast\_repo\_path = "../../../../../my\_feature\_repo/feature\_repo/"  
store = FeatureStore(repo\_path=feast\_repo\_path)  

```

### Prompts[​](#prompts "Direct link to Prompts")

Here we will set up a custom FeastPromptTemplate. This prompt template will take in a driver id, look up their stats, and format those stats into a prompt.

Note that the input to this prompt template is just `driver_id`, since that is the only user defined piece (all other variables are looked up inside the prompt template).

```python
from langchain.prompts import PromptTemplate, StringPromptTemplate  

```

```python
template = """Given the driver's up to date stats, write them note relaying those stats to them.  
If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better  
  
Here are the drivers stats:  
Conversation rate: {conv\_rate}  
Acceptance rate: {acc\_rate}  
Average Daily Trips: {avg\_daily\_trips}  
  
Your response:"""  
prompt = PromptTemplate.from\_template(template)  

```

```python
class FeastPromptTemplate(StringPromptTemplate):  
 def format(self, \*\*kwargs) -> str:  
 driver\_id = kwargs.pop("driver\_id")  
 feature\_vector = store.get\_online\_features(  
 features=[  
 "driver\_hourly\_stats:conv\_rate",  
 "driver\_hourly\_stats:acc\_rate",  
 "driver\_hourly\_stats:avg\_daily\_trips",  
 ],  
 entity\_rows=[{"driver\_id": driver\_id}],  
 ).to\_dict()  
 kwargs["conv\_rate"] = feature\_vector["conv\_rate"][0]  
 kwargs["acc\_rate"] = feature\_vector["acc\_rate"][0]  
 kwargs["avg\_daily\_trips"] = feature\_vector["avg\_daily\_trips"][0]  
 return prompt.format(\*\*kwargs)  

```

```python
prompt\_template = FeastPromptTemplate(input\_variables=["driver\_id"])  

```

```python
print(prompt\_template.format(driver\_id=1001))  

```

```text
 Given the driver's up to date stats, write them note relaying those stats to them.  
 If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better  
   
 Here are the drivers stats:  
 Conversation rate: 0.4745151400566101  
 Acceptance rate: 0.055561766028404236  
 Average Daily Trips: 936  
   
 Your response:  

```

### Use in a chain[​](#use-in-a-chain "Direct link to Use in a chain")

We can now use this in a chain, successfully creating a chain that achieves personalization backed by a feature store.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import LLMChain  

```

```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt\_template)  

```

```python
chain.run(1001)  

```

```text
 "Hi there! I wanted to update you on your current stats. Your acceptance rate is 0.055561766028404236 and your average daily trips are 936. While your conversation rate is currently 0.4745151400566101, I have no doubt that with a little extra effort, you'll be able to exceed that .5 mark! Keep up the great work! And remember, even chickens can't always cross the road, but they still give it their best shot."  

```

## Tecton[​](#tecton "Direct link to Tecton")

Above, we showed how you could use Feast, a popular open-source and self-managed feature store, with LangChain. Our examples below will show a similar integration using Tecton. Tecton is a fully managed feature platform built to orchestrate the complete ML feature lifecycle, from transformation to online serving, with enterprise-grade SLAs.

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

- Tecton Deployment (sign up at <https://tecton.ai>)
- `TECTON_API_KEY` environment variable set to a valid Service Account key

### Define and load features[​](#define-and-load-features "Direct link to Define and load features")

We will use the user_transaction_counts Feature View from the [Tecton tutorial](https://docs.tecton.ai/docs/tutorials/tecton-fundamentals) as part of a Feature Service. For simplicity, we are only using a single Feature View; however, more sophisticated applications may require more feature views to retrieve the features needed for its prompt.

```python
user\_transaction\_metrics = FeatureService(  
 name = "user\_transaction\_metrics",  
 features = [user\_transaction\_counts]  
)  

```

The above Feature Service is expected to be [applied to a live workspace](https://docs.tecton.ai/docs/applying-feature-repository-changes-to-a-workspace). For this example, we will be using the "prod" workspace.

```python
import tecton  
  
workspace = tecton.get\_workspace("prod")  
feature\_service = workspace.get\_feature\_service("user\_transaction\_metrics")  

```

### Prompts[​](#prompts-1 "Direct link to Prompts")

Here we will set up a custom TectonPromptTemplate. This prompt template will take in a user_id , look up their stats, and format those stats into a prompt.

Note that the input to this prompt template is just `user_id`, since that is the only user defined piece (all other variables are looked up inside the prompt template).

```python
from langchain.prompts import PromptTemplate, StringPromptTemplate  

```

```python
template = """Given the vendor's up to date transaction stats, write them a note based on the following rules:  
  
1. If they had a transaction in the last day, write a short congratulations message on their recent sales  
2. If no transaction in the last day, but they had a transaction in the last 30 days, playfully encourage them to sell more.  
3. Always add a silly joke about chickens at the end  
  
Here are the vendor's stats:  
Number of Transactions Last Day: {transaction\_count\_1d}  
Number of Transactions Last 30 Days: {transaction\_count\_30d}  
  
Your response:"""  
prompt = PromptTemplate.from\_template(template)  

```

```python
class TectonPromptTemplate(StringPromptTemplate):  
 def format(self, \*\*kwargs) -> str:  
 user\_id = kwargs.pop("user\_id")  
 feature\_vector = feature\_service.get\_online\_features(  
 join\_keys={"user\_id": user\_id}  
 ).to\_dict()  
 kwargs["transaction\_count\_1d"] = feature\_vector[  
 "user\_transaction\_counts.transaction\_count\_1d\_1d"  
 ]  
 kwargs["transaction\_count\_30d"] = feature\_vector[  
 "user\_transaction\_counts.transaction\_count\_30d\_1d"  
 ]  
 return prompt.format(\*\*kwargs)  

```

```python
prompt\_template = TectonPromptTemplate(input\_variables=["user\_id"])  

```

```python
print(prompt\_template.format(user\_id="user\_469998441571"))  

```

```text
 Given the vendor's up to date transaction stats, write them a note based on the following rules:  
   
 1. If they had a transaction in the last day, write a short congratulations message on their recent sales  
 2. If no transaction in the last day, but they had a transaction in the last 30 days, playfully encourage them to sell more.  
 3. Always add a silly joke about chickens at the end  
   
 Here are the vendor's stats:  
 Number of Transactions Last Day: 657  
 Number of Transactions Last 30 Days: 20326  
   
 Your response:  

```

### Use in a chain[​](#use-in-a-chain-1 "Direct link to Use in a chain")

We can now use this in a chain, successfully creating a chain that achieves personalization backed by the Tecton Feature Platform.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import LLMChain  

```

```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt\_template)  

```

```python
chain.run("user\_469998441571")  

```

```text
 'Wow, congratulations on your recent sales! Your business is really soaring like a chicken on a hot air balloon! Keep up the great work!'  

```

## Featureform[​](#featureform "Direct link to Featureform")

Finally, we will use [Featureform](https://github.com/featureform/featureform), an open-source and enterprise-grade feature store, to run the same example. Featureform allows you to work with your infrastructure like Spark or locally to define your feature transformations.

### Initialize Featureform[​](#initialize-featureform "Direct link to Initialize Featureform")

You can follow in the instructions in the README to initialize your transformations and features in Featureform.

```python
import featureform as ff  
  
client = ff.Client(host="demo.featureform.com")  

```

### Prompts[​](#prompts-2 "Direct link to Prompts")

Here we will set up a custom FeatureformPromptTemplate. This prompt template will take in the average amount a user pays per transactions.

Note that the input to this prompt template is just avg_transaction, since that is the only user defined piece (all other variables are looked up inside the prompt template).

```python
from langchain.prompts import PromptTemplate, StringPromptTemplate  

```

```python
template = """Given the amount a user spends on average per transaction, let them know if they are a high roller. Otherwise, make a silly joke about chickens at the end to make them feel better  
  
Here are the user's stats:  
Average Amount per Transaction: ${avg\_transcation}  
  
Your response:"""  
prompt = PromptTemplate.from\_template(template)  

```

```python
class FeatureformPromptTemplate(StringPromptTemplate):  
 def format(self, \*\*kwargs) -> str:  
 user\_id = kwargs.pop("user\_id")  
 fpf = client.features([("avg\_transactions", "quickstart")], {"user": user\_id})  
 return prompt.format(\*\*kwargs)  

```

```python
prompt\_template = FeatureformPromptTemplate(input\_variables=["user\_id"])  

```

```python
print(prompt\_template.format(user\_id="C1410926"))  

```

### Use in a chain[​](#use-in-a-chain-2 "Direct link to Use in a chain")

We can now use this in a chain, successfully creating a chain that achieves personalization backed by the Featureform Feature Platform.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import LLMChain  

```

```python
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt\_template)  

```

```python
chain.run("C1410926")  

```

## AzureML Managed Feature Store[​](#azureml-managed-feature-store "Direct link to AzureML Managed Feature Store")

We will use [AzureML Managed Feature Store](https://learn.microsoft.com/en-us/azure/machine-learning/concept-what-is-managed-feature-store) to run the example below.

### Prerequisites[​](#prerequisites-1 "Direct link to Prerequisites")

- Create feature store with online materialization using instructions here [Enable online materialization and run online inference](https://github.com/Azure/azureml-examples/blob/featurestore/online/sdk/python/featurestore_sample/notebooks/sdk_only/5.%20Enable%20online%20store%20and%20run%20online%20inference.ipynb).
- A successfully created feature store by following the instructions should have an `account` featureset with version as `1`. It will have `accountID` as index column with features `accountAge`, `accountCountry`, `numPaymentRejects1dPerUser`.

Create feature store with online materialization using instructions here [Enable online materialization and run online inference](https://github.com/Azure/azureml-examples/blob/featurestore/online/sdk/python/featurestore_sample/notebooks/sdk_only/5.%20Enable%20online%20store%20and%20run%20online%20inference.ipynb).

A successfully created feature store by following the instructions should have an `account` featureset with version as `1`. It will have `accountID` as index column with features `accountAge`, `accountCountry`, `numPaymentRejects1dPerUser`.

### Prompts[​](#prompts-3 "Direct link to Prompts")

- Here we will set up a custom AzureMLFeatureStorePromptTemplate. This prompt template will take in an `account_id` and optional `query`. It then fetches feature values from feature store and format those features into the output prompt. Note that the required input to this prompt template is just `account_id`, since that is the only user defined piece (all other variables are looked up inside the prompt template).
- Also note that this is a bootstrap example to showcase how LLM applications can leverage AzureML managed feature store. Developers are welcome to improve the prompt template further to suit their needs.

Here we will set up a custom AzureMLFeatureStorePromptTemplate. This prompt template will take in an `account_id` and optional `query`. It then fetches feature values from feature store and format those features into the output prompt. Note that the required input to this prompt template is just `account_id`, since that is the only user defined piece (all other variables are looked up inside the prompt template).

Also note that this is a bootstrap example to showcase how LLM applications can leverage AzureML managed feature store. Developers are welcome to improve the prompt template further to suit their needs.

```python
import os  
os.environ['AZURE\_ML\_CLI\_PRIVATE\_FEATURES\_ENABLED'] = 'True'  

```

```python
import pandas  
  
from pydantic import Extra  
from langchain.prompts import PromptTemplate, StringPromptTemplate  
from azure.identity import AzureCliCredential  
from azureml.featurestore import FeatureStoreClient, init\_online\_lookup, get\_online\_features  
  
class AzureMLFeatureStorePromptTemplate(StringPromptTemplate, extra=Extra.allow):  
  
 def \_\_init\_\_(self, subscription\_id: str, resource\_group: str, feature\_store\_name: str, \*\*kwargs):  
 # this is an example template for proof of concept and can be changed to suit the developer needs  
 template = """  
 {query}  
 ###  
 account id = {account\_id}  
 account age = {account\_age}  
 account country = {account\_country}  
 payment rejects 1d per user = {payment\_rejects\_1d\_per\_user}  
 ###  
 """  
 prompt\_template=PromptTemplate.from\_template(template)  
 super().\_\_init\_\_(prompt=prompt\_template, input\_variables=["account\_id", "query"])  
  
 # use AzureMLOnBehalfOfCredential() in spark context  
 credential = AzureCliCredential()  
  
 self.\_fs\_client = FeatureStoreClient(  
 credential=credential,  
 subscription\_id=subscription\_id,  
 resource\_group\_name=resource\_group,  
 name=feature\_store\_name)  
   
 self.\_feature\_set = self.\_fs\_client.feature\_sets.get(name="accounts", version=1)  
  
 init\_online\_lookup(self.\_feature\_set.features, credential, force=True)  
   
  
 def format(self, \*\*kwargs) -> str:   
 if "account\_id" not in kwargs:  
 raise "account\_id needed to fetch details from feature store"  
 account\_id = kwargs.pop("account\_id")   
  
 query=""  
 if "query" in kwargs:  
 query = kwargs.pop("query")  
  
 # feature set is registered with accountID as entity index column.  
 obs = pandas.DataFrame({'accountID': [account\_id]})  
  
 # get the feature details for the input entity from feature store.  
 df = get\_online\_features(self.\_feature\_set.features, obs)   
  
 # populate prompt template output using the fetched feature values.  
 kwargs["query"] = query  
 kwargs["account\_id"] = account\_id  
 kwargs["account\_age"] = df["accountAge"][0]  
 kwargs["account\_country"] = df["accountCountry"][0]  
 kwargs["payment\_rejects\_1d\_per\_user"] = df["numPaymentRejects1dPerUser"][0]  
  
 return self.prompt.format(\*\*kwargs)  

```

### Test[​](#test "Direct link to Test")

```python
# Replace the place holders below with actual details of feature store that was created in previous steps  
  
prompt\_template = AzureMLFeatureStorePromptTemplate(  
 subscription\_id="",  
 resource\_group="",  
 feature\_store\_name="")  

```

```python
print(prompt\_template.format(account\_id="A1829581630230790"))  

```

```text
   
   
 ###  
 account id = A1829581630230790  
 account age = 563.0  
 account country = GB  
 payment rejects 1d per user = 15.0  
 ###  
   

```

### Use in a chain[​](#use-in-a-chain-3 "Direct link to Use in a chain")

We can now use this in a chain, successfully creating a chain that achieves personalization backed by the AzureML Managed Feature Store.

```python
os.environ["OPENAI\_API\_KEY"]="" # Fill the open ai key here  
  
from langchain.chat\_models import ChatOpenAI  
from langchain.chains import LLMChain  
  
chain = LLMChain(llm=ChatOpenAI(), prompt=prompt\_template)  

```

```python
# NOTE: developer's can further fine tune AzureMLFeatureStorePromptTemplate  
# for getting even more accurate results for the input query  
chain.predict(account\_id="A1829581630230790", query ="write a small thank you note within 20 words if account age > 10 using the account stats")  

```

```text
 'Thank you for being a valued member for over 10 years! We appreciate your continued support.'  

```

- [Feast](#feast)

  - [Load Feast Store](#load-feast-store)
  - [Prompts](#prompts)
  - [Use in a chain](#use-in-a-chain)

- [Tecton](#tecton)

  - [Prerequisites](#prerequisites)
  - [Define and load features](#define-and-load-features)
  - [Prompts](#prompts-1)
  - [Use in a chain](#use-in-a-chain-1)

- [Featureform](#featureform)

  - [Initialize Featureform](#initialize-featureform)
  - [Prompts](#prompts-2)
  - [Use in a chain](#use-in-a-chain-2)

- [AzureML Managed Feature Store](#azureml-managed-feature-store)

  - [Prerequisites](#prerequisites-1)
  - [Prompts](#prompts-3)
  - [Test](#test)
  - [Use in a chain](#use-in-a-chain-3)

- [Load Feast Store](#load-feast-store)

- [Prompts](#prompts)

- [Use in a chain](#use-in-a-chain)

- [Prerequisites](#prerequisites)

- [Define and load features](#define-and-load-features)

- [Prompts](#prompts-1)

- [Use in a chain](#use-in-a-chain-1)

- [Initialize Featureform](#initialize-featureform)

- [Prompts](#prompts-2)

- [Use in a chain](#use-in-a-chain-2)

- [Prerequisites](#prerequisites-1)

- [Prompts](#prompts-3)

- [Test](#test)

- [Use in a chain](#use-in-a-chain-3)
