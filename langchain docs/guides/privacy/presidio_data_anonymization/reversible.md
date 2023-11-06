# Reversible anonymization

# Reversible data anonymization with Microsoft Presidio

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/privacy/presidio_data_anonymization/reversible.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

## Use case[​](#use-case "Direct link to Use case")

We have already written about the importance of anonymizing sensitive data in the previous section. **Reversible Anonymization** is an equally essential technology while sharing information with language models, as it balances data protection with data usability. This technique involves masking sensitive personally identifiable information (PII), yet it can be reversed and original data can be restored when authorized users need it. Its main advantage lies in the fact that while it conceals individual identities to prevent misuse, it also allows the concealed data to be accurately unmasked should it be necessary for legal or compliance purposes.

## Overview[​](#overview "Direct link to Overview")

We implemented the `PresidioReversibleAnonymizer`, which consists of two parts:

1. anonymization - it works the same way as `PresidioAnonymizer`, plus the object itself stores a mapping of made-up values to original ones, for example:

```text
 {  
 "PERSON": {  
 "<anonymized>": "<original>",  
 "John Doe": "Slim Shady"  
 },  
 "PHONE\_NUMBER": {  
 "111-111-1111": "555-555-5555"  
 }  
 ...  
 }  

```

2. deanonymization - using the mapping described above, it matches fake data with original data and then substitutes it.

Between anonymization and deanonymization user can perform different operations, for example, passing the output to LLM.

## Quickstart[​](#quickstart "Direct link to Quickstart")

```python
# Install necessary packages  
# ! pip install langchain langchain-experimental openai presidio-analyzer presidio-anonymizer spacy Faker  
# ! python -m spacy download en\_core\_web\_lg  

```

`PresidioReversibleAnonymizer` is not significantly different from its predecessor (`PresidioAnonymizer`) in terms of anonymization:

```python
from langchain\_experimental.data\_anonymizer import PresidioReversibleAnonymizer  
  
anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON", "PHONE\_NUMBER", "EMAIL\_ADDRESS", "CREDIT\_CARD"],  
 # Faker seed is used here to make sure the same fake data is generated for the test purposes  
 # In production, it is recommended to remove the faker\_seed parameter (it will default to None)  
 faker\_seed=42,  
)  
  
anonymizer.anonymize(  
 "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com. "  
 "By the way, my card number is: 4916 0387 9536 0861"  
)  

```

```text
 'My name is Maria Lynch, call me at 7344131647 or email me at jamesmichael@example.com. By the way, my card number is: 4838637940262'  

```

This is what the full string we want to deanonymize looks like:

```python
# We know this data, as we set the faker\_seed parameter  
fake\_name = "Maria Lynch"  
fake\_phone = "7344131647"  
fake\_email = "jamesmichael@example.com"  
fake\_credit\_card = "4838637940262"  
  
anonymized\_text = f"""{fake\_name} recently lost his wallet.   
Inside is some cash and his credit card with the number {fake\_credit\_card}.   
If you would find it, please call at {fake\_phone} or write an email here: {fake\_email}.  
{fake\_name} would be very grateful!"""  
  
print(anonymized\_text)  

```

```text
 Maria Lynch recently lost his wallet.   
 Inside is some cash and his credit card with the number 4838637940262.   
 If you would find it, please call at 7344131647 or write an email here: jamesmichael@example.com.  
 Maria Lynch would be very grateful!  

```

And now, using the `deanonymize` method, we can reverse the process:

```python
print(anonymizer.deanonymize(anonymized\_text))  

```

```text
 Slim Shady recently lost his wallet.   
 Inside is some cash and his credit card with the number 4916 0387 9536 0861.   
 If you would find it, please call at 313-666-7440 or write an email here: real.slim.shady@gmail.com.  
 Slim Shady would be very grateful!  

```

### Using with LangChain Expression Language[​](#using-with-langchain-expression-language "Direct link to Using with LangChain Expression Language")

With LCEL we can easily chain together anonymization and deanonymization with the rest of our application. This is an example of using the anonymization mechanism with a query to LLM (without deanonymization for now):

```python
text = f"""Slim Shady recently lost his wallet.   
Inside is some cash and his credit card with the number 4916 0387 9536 0861.   
If you would find it, please call at 313-666-7440 or write an email here: real.slim.shady@gmail.com."""  

```

```python
from langchain.prompts.prompt import PromptTemplate  
from langchain.chat\_models import ChatOpenAI  
  
anonymizer = PresidioReversibleAnonymizer()  
  
template = """Rewrite this text into an official, short email:  
  
{anonymized\_text}"""  
prompt = PromptTemplate.from\_template(template)  
llm = ChatOpenAI(temperature=0)  
  
chain = {"anonymized\_text": anonymizer.anonymize} | prompt | llm  
response = chain.invoke(text)  
print(response.content)  

```

```text
 Dear Sir/Madam,  
   
 We regret to inform you that Monique Turner has recently misplaced his wallet, which contains a sum of cash and his credit card with the number 213152056829866.   
   
 If you happen to come across this wallet, kindly contact us at (770)908-7734x2835 or send an email to barbara25@example.net.  
   
 Thank you for your cooperation.  
   
 Sincerely,  
 [Your Name]  

```

Now, let's add **deanonymization step** to our sequence:

```python
chain = chain | (lambda ai\_message: anonymizer.deanonymize(ai\_message.content))  
response = chain.invoke(text)  
print(response)  

```

```text
 Dear Sir/Madam,  
   
 We regret to inform you that Slim Shady has recently misplaced his wallet, which contains a sum of cash and his credit card with the number 4916 0387 9536 0861.   
   
 If you happen to come across this wallet, kindly contact us at 313-666-7440 or send an email to real.slim.shady@gmail.com.  
   
 Thank you for your cooperation.  
   
 Sincerely,  
 [Your Name]  

```

Anonymized data was given to the model itself, and therefore it was protected from being leaked to the outside world. Then, the model's response was processed, and the factual value was replaced with the real one.

## Extra knowledge[​](#extra-knowledge "Direct link to Extra knowledge")

`PresidioReversibleAnonymizer` stores the mapping of the fake values to the original values in the `deanonymizer_mapping` parameter, where key is fake PII and value is the original one:

```python
from langchain\_experimental.data\_anonymizer import PresidioReversibleAnonymizer  
  
anonymizer = PresidioReversibleAnonymizer(  
 analyzed\_fields=["PERSON", "PHONE\_NUMBER", "EMAIL\_ADDRESS", "CREDIT\_CARD"],  
 # Faker seed is used here to make sure the same fake data is generated for the test purposes  
 # In production, it is recommended to remove the faker\_seed parameter (it will default to None)  
 faker\_seed=42,  
)  
  
anonymizer.anonymize(  
 "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com. "  
 "By the way, my card number is: 4916 0387 9536 0861"  
)  
  
anonymizer.deanonymizer\_mapping  

```

```text
 {'PERSON': {'Maria Lynch': 'Slim Shady'},  
 'PHONE\_NUMBER': {'7344131647': '313-666-7440'},  
 'EMAIL\_ADDRESS': {'jamesmichael@example.com': 'real.slim.shady@gmail.com'},  
 'CREDIT\_CARD': {'4838637940262': '4916 0387 9536 0861'}}  

```

Anonymizing more texts will result in new mapping entries:

```python
print(  
 anonymizer.anonymize(  
 "Do you have his VISA card number? Yep, it's 4001 9192 5753 7193. I'm John Doe by the way."  
 )  
)  
  
anonymizer.deanonymizer\_mapping  

```

```text
 Do you have his VISA card number? Yep, it's 3537672423884966. I'm William Bowman by the way.  
  
  
  
  
  
 {'PERSON': {'Maria Lynch': 'Slim Shady', 'William Bowman': 'John Doe'},  
 'PHONE\_NUMBER': {'7344131647': '313-666-7440'},  
 'EMAIL\_ADDRESS': {'jamesmichael@example.com': 'real.slim.shady@gmail.com'},  
 'CREDIT\_CARD': {'4838637940262': '4916 0387 9536 0861',  
 '3537672423884966': '4001 9192 5753 7193'}}  

```

Thanks to the built-in memory, entities that have already been detected and anonymised will take the same form in subsequent processed texts, so no duplicates will exist in the mapping:

```python
print(  
 anonymizer.anonymize(  
 "My VISA card number is 4001 9192 5753 7193 and my name is John Doe."  
 )  
)  
  
anonymizer.deanonymizer\_mapping  

```

```text
 My VISA card number is 3537672423884966 and my name is William Bowman.  
  
  
  
  
  
 {'PERSON': {'Maria Lynch': 'Slim Shady', 'William Bowman': 'John Doe'},  
 'PHONE\_NUMBER': {'7344131647': '313-666-7440'},  
 'EMAIL\_ADDRESS': {'jamesmichael@example.com': 'real.slim.shady@gmail.com'},  
 'CREDIT\_CARD': {'4838637940262': '4916 0387 9536 0861',  
 '3537672423884966': '4001 9192 5753 7193'}}  

```

We can save the mapping itself to a file for future use:

```python
# We can save the deanonymizer mapping as a JSON or YAML file  
  
anonymizer.save\_deanonymizer\_mapping("deanonymizer\_mapping.json")  
# anonymizer.save\_deanonymizer\_mapping("deanonymizer\_mapping.yaml")  

```

And then, load it in another `PresidioReversibleAnonymizer` instance:

```python
anonymizer = PresidioReversibleAnonymizer()  
  
anonymizer.deanonymizer\_mapping  

```

```text
 {}  

```

```python
anonymizer.load\_deanonymizer\_mapping("deanonymizer\_mapping.json")  
  
anonymizer.deanonymizer\_mapping  

```

```text
 {'PERSON': {'Maria Lynch': 'Slim Shady', 'William Bowman': 'John Doe'},  
 'PHONE\_NUMBER': {'7344131647': '313-666-7440'},  
 'EMAIL\_ADDRESS': {'jamesmichael@example.com': 'real.slim.shady@gmail.com'},  
 'CREDIT\_CARD': {'4838637940262': '4916 0387 9536 0861',  
 '3537672423884966': '4001 9192 5753 7193'}}  

```

### Custom deanonymization strategy[​](#custom-deanonymization-strategy "Direct link to Custom deanonymization strategy")

The default deanonymization strategy is to exactly match the substring in the text with the mapping entry. Due to the indeterminism of LLMs, it may be that the model will change the format of the private data slightly or make a typo, for example:

- *Keanu Reeves* -> *Kaenu Reeves*
- *John F. Kennedy* -> *John Kennedy*
- *Main St, New York* -> *New York*

It is therefore worth considering appropriate prompt engineering (have the model return PII in unchanged format) or trying to implement your replacing strategy. For example, you can use fuzzy matching - this will solve problems with typos and minor changes in the text. Some implementations of the swapping strategy can be found in the file `deanonymizer_matching_strategies.py`.

```python
from langchain\_experimental.data\_anonymizer.deanonymizer\_matching\_strategies import (  
 case\_insensitive\_matching\_strategy,  
)  
  
# Original name: Maria Lynch  
print(anonymizer.deanonymize("maria lynch"))  
print(  
 anonymizer.deanonymize(  
 "maria lynch", deanonymizer\_matching\_strategy=case\_insensitive\_matching\_strategy  
 )  
)  

```

```text
 maria lynch  
 Slim Shady  

```

```python
from langchain\_experimental.data\_anonymizer.deanonymizer\_matching\_strategies import (  
 fuzzy\_matching\_strategy,  
)  
  
# Original name: Maria Lynch  
# Original phone number: 7344131647 (without dashes)  
print(anonymizer.deanonymize("Call Maria K. Lynch at 734-413-1647"))  
print(  
 anonymizer.deanonymize(  
 "Call Maria K. Lynch at 734-413-1647",  
 deanonymizer\_matching\_strategy=fuzzy\_matching\_strategy,  
 )  
)  

```

```text
 Call Maria K. Lynch at 734-413-1647  
 Call Slim Shady at 313-666-7440  

```

It seems that the combined method works best:

- first apply the exact match strategy
- then match the rest using the fuzzy strategy

```python
from langchain\_experimental.data\_anonymizer.deanonymizer\_matching\_strategies import (  
 combined\_exact\_fuzzy\_matching\_strategy,  
)  
  
# Changed some values for fuzzy match showcase:  
# - "Maria Lynch" -> "Maria K. Lynch"  
# - "7344131647" -> "734-413-1647"  
# - "213186379402654" -> "2131 8637 9402 654"  
print(  
 anonymizer.deanonymize(  
 (  
 "Are you Maria F. Lynch? I found your card with number 4838 6379 40262.\n"  
 "Is this your phone number: 734-413-1647?\n"  
 "Is this your email address: wdavis@example.net"  
 ),  
 deanonymizer\_matching\_strategy=combined\_exact\_fuzzy\_matching\_strategy,  
 )  
)  

```

```text
 Are you Slim Shady? I found your card with number 4916 0387 9536 0861.  
 Is this your phone number: 313-666-7440?  
 Is this your email address: wdavis@example.net  

```

Of course, there is no perfect method and it is worth experimenting and finding the one best suited to your use case.

## Future works[​](#future-works "Direct link to Future works")

- **better matching and substitution of fake values for real ones** - currently the strategy is based on matching full strings and then substituting them. Due to the indeterminism of language models, it may happen that the value in the answer is slightly changed (e.g. *John Doe* -> *John* or *Main St, New York* -> *New York*) and such a substitution is then no longer possible. Therefore, it is worth adjusting the matching for your needs.

- [Use case](#use-case)

- [Overview](#overview)

- [Quickstart](#quickstart)

  - [Using with LangChain Expression Language](#using-with-langchain-expression-language)

- [Extra knowledge](#extra-knowledge)

  - [Custom deanonymization strategy](#custom-deanonymization-strategy)

- [Future works](#future-works)

- [Using with LangChain Expression Language](#using-with-langchain-expression-language)

- [Custom deanonymization strategy](#custom-deanonymization-strategy)
