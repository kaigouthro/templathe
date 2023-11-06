# QA with private data protection

# QA with private data protection

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/privacy/presidio_data_anonymization/qa_privacy_protection.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

In this notebook, we will look at building a basic system for question answering, based on private data. Before feeding the LLM with this data, we need to protect it so that it doesn't go to an external API (e.g. OpenAI, Anthropic). Then, after receiving the model output, we would like the data to be restored to its original form. Below you can observe an example flow of this QA system:

![](/img/qa_privacy_protection.png)

In the following notebook, we will not go into the details of how the anonymizer works. If you are interested, please visit [this part of the documentation](https://python.langchain.com/docs/guides/privacy/presidio_data_anonymization/).

## Quickstart[​](#quickstart "Direct link to Quickstart")

### Iterative process of upgrading the anonymizer[​](#iterative-process-of-upgrading-the-anonymizer "Direct link to Iterative process of upgrading the anonymizer")

```python
# Install necessary packages  
# !pip install langchain langchain-experimental openai presidio-analyzer presidio-anonymizer spacy Faker faiss-cpu tiktoken  
# ! python -m spacy download en\_core\_web\_lg  

```

```python
document\_content = """Date: October 19, 2021  
 Witness: John Doe  
 Subject: Testimony Regarding the Loss of Wallet  
  
 Testimony Content:  
  
 Hello Officer,  
  
 My name is John Doe and on October 19, 2021, my wallet was stolen in the vicinity of Kilmarnock during a bike trip. This wallet contains some very important things to me.  
  
 Firstly, the wallet contains my credit card with number 4111 1111 1111 1111, which is registered under my name and linked to my bank account, PL61109010140000071219812874.  
  
 Additionally, the wallet had a driver's license - DL No: 999000680 issued to my name. It also houses my Social Security Number, 602-76-4532.   
  
 What's more, I had my polish identity card there, with the number ABC123456.  
  
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at 9:30 AM.  
  
 In case any information arises regarding my wallet, please reach out to me on my phone number, 999-888-7777, or through my personal email, johndoe@example.com.  
  
 Please consider this information to be highly confidential and respect my privacy.   
  
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, support@bankname.com.  
 My representative there is Victoria Cherry (her business phone: 987-654-3210).  
  
 Thank you for your assistance,  
  
 John Doe"""  

```

```python
from langchain.schema import Document  
  
documents = [Document(page\_content=document\_content)]  

```

We only have one document, so before we move on to creating a QA system, let's focus on its content to begin with.

You may observe that the text contains many different PII values, some types occur repeatedly (names, phone numbers, emails), and some specific PIIs are repeated (John Doe).

```python
# Util function for coloring the PII markers  
# NOTE: It will not be visible on documentation page, only in the notebook  
import re  
  
  
def print\_colored\_pii(string):  
 colored\_string = re.sub(  
 r"(<[^>]\*>)", lambda m: "\033[31m" + m.group(1) + "\033[0m", string  
 )  
 print(colored\_string)  

```

Let's proceed and try to anonymize the text with the default settings. For now, we don't replace the data with synthetic, we just mark it with markers (e.g. `<PERSON>`), so we set `add_default_faker_operators=False`:

```python
from langchain\_experimental.data\_anonymizer import PresidioReversibleAnonymizer  
  
anonymizer = PresidioReversibleAnonymizer(  
 add\_default\_faker\_operators=False,  
)  
  
print\_colored\_pii(anonymizer.anonymize(document\_content))  

```

```text
 Date: <DATE\_TIME>  
 Witness: <PERSON>  
 Subject: Testimony Regarding the Loss of Wallet  
   
 Testimony Content:  
   
 Hello Officer,  
   
 My name is <PERSON> and on <DATE\_TIME>, my wallet was stolen in the vicinity of <LOCATION> during a bike trip. This wallet contains some very important things to me.  
   
 Firstly, the wallet contains my credit card with number <CREDIT\_CARD>, which is registered under my name and linked to my bank account, <IBAN\_CODE>.  
   
 Additionally, the wallet had a driver's license - DL No: <US\_DRIVER\_LICENSE> issued to my name. It also houses my Social Security Number, <US\_SSN>.   
   
 What's more, I had my polish identity card there, with the number ABC123456.  
   
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at <DATE\_TIME\_2>.  
   
 In case any information arises regarding my wallet, please reach out to me on my phone number, <PHONE\_NUMBER>, or through my personal email, <EMAIL\_ADDRESS>.  
   
 Please consider this information to be highly confidential and respect my privacy.   
   
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, <EMAIL\_ADDRESS\_2>.  
 My representative there is <PERSON\_2> (her business phone: <UK\_NHS>).  
   
 Thank you for your assistance,  
   
 <PERSON>  

```

Let's also look at the mapping between original and anonymized values:

```python
import pprint  
  
pprint.pprint(anonymizer.deanonymizer\_mapping)  

```

```text
 {'CREDIT\_CARD': {'<CREDIT\_CARD>': '4111 1111 1111 1111'},  
 'DATE\_TIME': {'<DATE\_TIME>': 'October 19, 2021', '<DATE\_TIME\_2>': '9:30 AM'},  
 'EMAIL\_ADDRESS': {'<EMAIL\_ADDRESS>': 'johndoe@example.com',  
 '<EMAIL\_ADDRESS\_2>': 'support@bankname.com'},  
 'IBAN\_CODE': {'<IBAN\_CODE>': 'PL61109010140000071219812874'},  
 'LOCATION': {'<LOCATION>': 'Kilmarnock'},  
 'PERSON': {'<PERSON>': 'John Doe', '<PERSON\_2>': 'Victoria Cherry'},  
 'PHONE\_NUMBER': {'<PHONE\_NUMBER>': '999-888-7777'},  
 'UK\_NHS': {'<UK\_NHS>': '987-654-3210'},  
 'US\_DRIVER\_LICENSE': {'<US\_DRIVER\_LICENSE>': '999000680'},  
 'US\_SSN': {'<US\_SSN>': '602-76-4532'}}  

```

In general, the anonymizer works pretty well, but I can observe two things to improve here:

1. Datetime redundancy - we have two different entities recognized as `DATE_TIME`, but they contain different type of information. The first one is a date (*October 19, 2021*), the second one is a time (*9:30 AM*). We can improve this by adding a new recognizer to the anonymizer, which will treat time separately from the date.
1. Polish ID - polish ID has unique pattern, which is not by default part of anonymizer recognizers. The value *ABC123456* is not anonymized.

The solution is simple: we need to add a new recognizers to the anonymizer. You can read more about it in [presidio documentation](https://microsoft.github.io/presidio/analyzer/adding_recognizers/).

Let's add new recognizers:

```python
# Define the regex pattern in a Presidio `Pattern` object:  
from presidio\_analyzer import Pattern, PatternRecognizer  
  
  
polish\_id\_pattern = Pattern(  
 name="polish\_id\_pattern",  
 regex="[A-Z]{3}\d{6}",  
 score=1,  
)  
time\_pattern = Pattern(  
 name="time\_pattern",  
 regex="(1[0-2]|0?[1-9]):[0-5][0-9] (AM|PM)",  
 score=1,  
)  
  
# Define the recognizer with one or more patterns  
polish\_id\_recognizer = PatternRecognizer(  
 supported\_entity="POLISH\_ID", patterns=[polish\_id\_pattern]  
)  
time\_recognizer = PatternRecognizer(supported\_entity="TIME", patterns=[time\_pattern])  

```

And now, we're adding recognizers to our anonymizer:

```python
anonymizer.add\_recognizer(polish\_id\_recognizer)  
anonymizer.add\_recognizer(time\_recognizer)  

```

Note that our anonymization instance remembers previously detected and anonymized values, including those that were not detected correctly (e.g., *"9:30 AM"* taken as `DATE_TIME`). So it's worth removing this value, or resetting the entire mapping now that our recognizers have been updated:

```python
anonymizer.reset\_deanonymizer\_mapping()  

```

Let's anonymize the text and see the results:

```python
print\_colored\_pii(anonymizer.anonymize(document\_content))  

```

```text
 Date: <DATE\_TIME>  
 Witness: <PERSON>  
 Subject: Testimony Regarding the Loss of Wallet  
   
 Testimony Content:  
   
 Hello Officer,  
   
 My name is <PERSON> and on <DATE\_TIME>, my wallet was stolen in the vicinity of <LOCATION> during a bike trip. This wallet contains some very important things to me.  
   
 Firstly, the wallet contains my credit card with number <CREDIT\_CARD>, which is registered under my name and linked to my bank account, <IBAN\_CODE>.  
   
 Additionally, the wallet had a driver's license - DL No: <US\_DRIVER\_LICENSE> issued to my name. It also houses my Social Security Number, <US\_SSN>.   
   
 What's more, I had my polish identity card there, with the number <POLISH\_ID>.  
   
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at <TIME>.  
   
 In case any information arises regarding my wallet, please reach out to me on my phone number, <PHONE\_NUMBER>, or through my personal email, <EMAIL\_ADDRESS>.  
   
 Please consider this information to be highly confidential and respect my privacy.   
   
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, <EMAIL\_ADDRESS\_2>.  
 My representative there is <PERSON\_2> (her business phone: <UK\_NHS>).  
   
 Thank you for your assistance,  
   
 <PERSON>  

```

```python
pprint.pprint(anonymizer.deanonymizer\_mapping)  

```

```text
 {'CREDIT\_CARD': {'<CREDIT\_CARD>': '4111 1111 1111 1111'},  
 'DATE\_TIME': {'<DATE\_TIME>': 'October 19, 2021'},  
 'EMAIL\_ADDRESS': {'<EMAIL\_ADDRESS>': 'johndoe@example.com',  
 '<EMAIL\_ADDRESS\_2>': 'support@bankname.com'},  
 'IBAN\_CODE': {'<IBAN\_CODE>': 'PL61109010140000071219812874'},  
 'LOCATION': {'<LOCATION>': 'Kilmarnock'},  
 'PERSON': {'<PERSON>': 'John Doe', '<PERSON\_2>': 'Victoria Cherry'},  
 'PHONE\_NUMBER': {'<PHONE\_NUMBER>': '999-888-7777'},  
 'POLISH\_ID': {'<POLISH\_ID>': 'ABC123456'},  
 'TIME': {'<TIME>': '9:30 AM'},  
 'UK\_NHS': {'<UK\_NHS>': '987-654-3210'},  
 'US\_DRIVER\_LICENSE': {'<US\_DRIVER\_LICENSE>': '999000680'},  
 'US\_SSN': {'<US\_SSN>': '602-76-4532'}}  

```

As you can see, our new recognizers work as expected. The anonymizer has replaced the time and Polish ID entities with the `<TIME>` and `<POLISH_ID>` markers, and the deanonymizer mapping has been updated accordingly.

Now, when all PII values are detected correctly, we can proceed to the next step, which is replacing the original values with synthetic ones. To do this, we need to set `add_default_faker_operators=True` (or just remove this parameter, because it's set to `True` by default):

```python
anonymizer = PresidioReversibleAnonymizer(  
 add\_default\_faker\_operators=True,  
 # Faker seed is used here to make sure the same fake data is generated for the test purposes  
 # In production, it is recommended to remove the faker\_seed parameter (it will default to None)  
 faker\_seed=42,  
)  
  
anonymizer.add\_recognizer(polish\_id\_recognizer)  
anonymizer.add\_recognizer(time\_recognizer)  
  
print\_colored\_pii(anonymizer.anonymize(document\_content))  

```

```text
 Date: 1986-04-18  
 Witness: Brian Cox DVM  
 Subject: Testimony Regarding the Loss of Wallet  
   
 Testimony Content:  
   
 Hello Officer,  
   
 My name is Brian Cox DVM and on 1986-04-18, my wallet was stolen in the vicinity of New Rita during a bike trip. This wallet contains some very important things to me.  
   
 Firstly, the wallet contains my credit card with number 6584801845146275, which is registered under my name and linked to my bank account, GB78GSWK37672423884969.  
   
 Additionally, the wallet had a driver's license - DL No: 781802744 issued to my name. It also houses my Social Security Number, 687-35-1170.   
   
 What's more, I had my polish identity card there, with the number <POLISH\_ID>.  
   
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at <TIME>.  
   
 In case any information arises regarding my wallet, please reach out to me on my phone number, 7344131647, or through my personal email, jamesmichael@example.com.  
   
 Please consider this information to be highly confidential and respect my privacy.   
   
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, blakeerik@example.com.  
 My representative there is Cristian Santos (her business phone: 2812140441).  
   
 Thank you for your assistance,  
   
 Brian Cox DVM  

```

As you can see, almost all values have been replaced with synthetic ones. The only exception is the Polish ID number and time, which are not supported by the default faker operators. We can add new operators to the anonymizer, which will generate random data. You can read more about custom operators [here](https://microsoft.github.io/presidio/tutorial/11_custom_anonymization/).

```python
from faker import Faker  
  
fake = Faker()  
  
  
def fake\_polish\_id(\_=None):  
 return fake.bothify(text="???######").upper()  
  
  
fake\_polish\_id()  

```

```text
 'VTC592627'  

```

```python
def fake\_time(\_=None):  
 return fake.time(pattern="%I:%M %p")  
  
  
fake\_time()  

```

```text
 '03:14 PM'  

```

Let's add newly created operators to the anonymizer:

```python
from presidio\_anonymizer.entities import OperatorConfig  
  
new\_operators = {  
 "POLISH\_ID": OperatorConfig("custom", {"lambda": fake\_polish\_id}),  
 "TIME": OperatorConfig("custom", {"lambda": fake\_time}),  
}  
  
anonymizer.add\_operators(new\_operators)  

```

And anonymize everything once again:

```python
anonymizer.reset\_deanonymizer\_mapping()  
print\_colored\_pii(anonymizer.anonymize(document\_content))  

```

```text
 Date: 1974-12-26  
 Witness: Jimmy Murillo  
 Subject: Testimony Regarding the Loss of Wallet  
   
 Testimony Content:  
   
 Hello Officer,  
   
 My name is Jimmy Murillo and on 1974-12-26, my wallet was stolen in the vicinity of South Dianeshire during a bike trip. This wallet contains some very important things to me.  
   
 Firstly, the wallet contains my credit card with number 213108121913614, which is registered under my name and linked to my bank account, GB17DBUR01326773602606.  
   
 Additionally, the wallet had a driver's license - DL No: 532311310 issued to my name. It also houses my Social Security Number, 690-84-1613.   
   
 What's more, I had my polish identity card there, with the number UFB745084.  
   
 I would like this data to be secured and protected in all possible ways. I believe It was stolen at 11:54 AM.  
   
 In case any information arises regarding my wallet, please reach out to me on my phone number, 876.931.1656, or through my personal email, briannasmith@example.net.  
   
 Please consider this information to be highly confidential and respect my privacy.   
   
 The bank has been informed about the stolen credit card and necessary actions have been taken from their end. They will be reachable at their official email, samuel87@example.org.  
 My representative there is Joshua Blair (her business phone: 3361388464).  
   
 Thank you for your assistance,  
   
 Jimmy Murillo  

```

```python
pprint.pprint(anonymizer.deanonymizer\_mapping)  

```

```text
 {'CREDIT\_CARD': {'213108121913614': '4111 1111 1111 1111'},  
 'DATE\_TIME': {'1974-12-26': 'October 19, 2021'},  
 'EMAIL\_ADDRESS': {'briannasmith@example.net': 'johndoe@example.com',  
 'samuel87@example.org': 'support@bankname.com'},  
 'IBAN\_CODE': {'GB17DBUR01326773602606': 'PL61109010140000071219812874'},  
 'LOCATION': {'South Dianeshire': 'Kilmarnock'},  
 'PERSON': {'Jimmy Murillo': 'John Doe', 'Joshua Blair': 'Victoria Cherry'},  
 'PHONE\_NUMBER': {'876.931.1656': '999-888-7777'},  
 'POLISH\_ID': {'UFB745084': 'ABC123456'},  
 'TIME': {'11:54 AM': '9:30 AM'},  
 'UK\_NHS': {'3361388464': '987-654-3210'},  
 'US\_DRIVER\_LICENSE': {'532311310': '999000680'},  
 'US\_SSN': {'690-84-1613': '602-76-4532'}}  

```

Voilà! Now all values are replaced with synthetic ones. Note that the deanonymizer mapping has been updated accordingly.

### Question-answering system with PII anonymization[​](#question-answering-system-with-pii-anonymization "Direct link to Question-answering system with PII anonymization")

Now, let's wrap it up together and create full question-answering system, based on `PresidioReversibleAnonymizer` and LangChain Expression Language (LCEL).

```python
# 1. Initialize anonymizer  
anonymizer = PresidioReversibleAnonymizer(  
 # Faker seed is used here to make sure the same fake data is generated for the test purposes  
 # In production, it is recommended to remove the faker\_seed parameter (it will default to None)  
 faker\_seed=42,  
)  
  
anonymizer.add\_recognizer(polish\_id\_recognizer)  
anonymizer.add\_recognizer(time\_recognizer)  
  
anonymizer.add\_operators(new\_operators)  

```

```python
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import FAISS  
  
# 2. Load the data: In our case data's already loaded  
# 3. Anonymize the data before indexing  
for doc in documents:  
 doc.page\_content = anonymizer.anonymize(doc.page\_content)  
  
# 4. Split the documents into chunks  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=1000, chunk\_overlap=100)  
chunks = text\_splitter.split\_documents(documents)  
  
# 5. Index the chunks (using OpenAI embeddings, because the data is already anonymized)  
embeddings = OpenAIEmbeddings()  
docsearch = FAISS.from\_documents(chunks, embeddings)  
retriever = docsearch.as\_retriever()  

```

```python
from operator import itemgetter  
from langchain.chat\_models.openai import ChatOpenAI  
from langchain.schema.runnable import RunnableMap  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema.output\_parser import StrOutputParser  
from langchain.schema.runnable import RunnablePassthrough  
from langchain.schema.runnable import RunnableLambda  
  
# 6. Create anonymizer chain  
template = """Answer the question based only on the following context:  
{context}  
  
Question: {anonymized\_question}  
"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
model = ChatOpenAI(temperature=0.3)  
  
  
\_inputs = RunnableMap(  
 question=RunnablePassthrough(),  
 # It is important to remember about question anonymization  
 anonymized\_question=RunnableLambda(anonymizer.anonymize),  
)  
  
anonymizer\_chain = (  
 \_inputs  
 | {  
 "context": itemgetter("anonymized\_question") | retriever,  
 "anonymized\_question": itemgetter("anonymized\_question"),  
 }  
 | prompt  
 | model  
 | StrOutputParser()  
)  

```

```python
anonymizer\_chain.invoke(  
 "Where did the theft of the wallet occur, at what time, and who was it stolen from?"  
)  

```

```text
 'The theft of the wallet occurred in the vicinity of New Rita during a bike trip. It was stolen from Brian Cox DVM. The time of the theft was 02:22 AM.'  

```

```python
# 7. Add deanonymization step to the chain  
chain\_with\_deanonymization = anonymizer\_chain | RunnableLambda(anonymizer.deanonymize)  
  
print(  
 chain\_with\_deanonymization.invoke(  
 "Where did the theft of the wallet occur, at what time, and who was it stolen from?"  
 )  
)  

```

```text
 The theft of the wallet occurred in the vicinity of Kilmarnock during a bike trip. It was stolen from John Doe. The time of the theft was 9:30 AM.  

```

```python
print(  
 chain\_with\_deanonymization.invoke("What was the content of the wallet in detail?")  
)  

```

```text
 The content of the wallet included a credit card with the number 4111 1111 1111 1111, registered under the name of John Doe and linked to the bank account PL61109010140000071219812874. It also contained a driver's license with the number 999000680 issued to John Doe, as well as his Social Security Number 602-76-4532. Additionally, the wallet had a Polish identity card with the number ABC123456.  

```

```python
print(chain\_with\_deanonymization.invoke("Whose phone number is it: 999-888-7777?"))  

```

```text
 The phone number 999-888-7777 belongs to John Doe.  

```

### Alternative approach: local embeddings + anonymizing the context after indexing[​](#alternative-approach-local-embeddings--anonymizing-the-context-after-indexing "Direct link to Alternative approach: local embeddings + anonymizing the context after indexing")

If for some reason you would like to index the data in its original form, or simply use custom embeddings, below is an example of how to do it:

```python
anonymizer = PresidioReversibleAnonymizer(  
 # Faker seed is used here to make sure the same fake data is generated for the test purposes  
 # In production, it is recommended to remove the faker\_seed parameter (it will default to None)  
 faker\_seed=42,  
)  
  
anonymizer.add\_recognizer(polish\_id\_recognizer)  
anonymizer.add\_recognizer(time\_recognizer)  
  
anonymizer.add\_operators(new\_operators)  

```

```python
from langchain.embeddings import HuggingFaceBgeEmbeddings  
  
model\_name = "BAAI/bge-base-en-v1.5"  
# model\_kwargs = {'device': 'cuda'}  
encode\_kwargs = {"normalize\_embeddings": True} # set True to compute cosine similarity  
local\_embeddings = HuggingFaceBgeEmbeddings(  
 model\_name=model\_name,  
 # model\_kwargs=model\_kwargs,  
 encode\_kwargs=encode\_kwargs,  
 query\_instruction="Represent this sentence for searching relevant passages:",  
)  

```

```python
documents = [Document(page\_content=document\_content)]  
  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=1000, chunk\_overlap=100)  
chunks = text\_splitter.split\_documents(documents)  
  
docsearch = FAISS.from\_documents(chunks, local\_embeddings)  
retriever = docsearch.as\_retriever()  

```

```python
template = """Answer the question based only on the following context:  
{context}  
  
Question: {anonymized\_question}  
"""  
prompt = ChatPromptTemplate.from\_template(template)  
  
model = ChatOpenAI(temperature=0.2)  

```

```python
from langchain.prompts.prompt import PromptTemplate  
from langchain.schema import format\_document  
  
DEFAULT\_DOCUMENT\_PROMPT = PromptTemplate.from\_template(template="{page\_content}")  
  
  
def \_combine\_documents(  
 docs, document\_prompt=DEFAULT\_DOCUMENT\_PROMPT, document\_separator="\n\n"  
):  
 doc\_strings = [format\_document(doc, document\_prompt) for doc in docs]  
 return document\_separator.join(doc\_strings)  
  
  
chain\_with\_deanonymization = (  
 RunnableMap({"question": RunnablePassthrough()})  
 | {  
 "context": itemgetter("question")  
 | retriever  
 | \_combine\_documents  
 | anonymizer.anonymize,  
 "anonymized\_question": lambda x: anonymizer.anonymize(x["question"]),  
 }  
 | prompt  
 | model  
 | StrOutputParser()  
 | RunnableLambda(anonymizer.deanonymize)  
)  

```

```python
print(  
 chain\_with\_deanonymization.invoke(  
 "Where did the theft of the wallet occur, at what time, and who was it stolen from?"  
 )  
)  

```

```text
 The theft of the wallet occurred in the vicinity of Kilmarnock during a bike trip. It was stolen from John Doe. The time of the theft was 9:30 AM.  

```

```python
print(  
 chain\_with\_deanonymization.invoke("What was the content of the wallet in detail?")  
)  

```

```text
 The content of the wallet included:  
 1. Credit card number: 4111 1111 1111 1111  
 2. Bank account number: PL61109010140000071219812874  
 3. Driver's license number: 999000680  
 4. Social Security Number: 602-76-4532  
 5. Polish identity card number: ABC123456  

```

```python
print(chain\_with\_deanonymization.invoke("Whose phone number is it: 999-888-7777?"))  

```

```text
 The phone number 999-888-7777 belongs to John Doe.  

```

- [Quickstart](#quickstart)

  - [Iterative process of upgrading the anonymizer](#iterative-process-of-upgrading-the-anonymizer)
  - [Question-answering system with PII anonymization](#question-answering-system-with-pii-anonymization)
  - [Alternative approach: local embeddings + anonymizing the context after indexing](#alternative-approach-local-embeddings--anonymizing-the-context-after-indexing)

- [Iterative process of upgrading the anonymizer](#iterative-process-of-upgrading-the-anonymizer)

- [Question-answering system with PII anonymization](#question-answering-system-with-pii-anonymization)

- [Alternative approach: local embeddings + anonymizing the context after indexing](#alternative-approach-local-embeddings--anonymizing-the-context-after-indexing)
