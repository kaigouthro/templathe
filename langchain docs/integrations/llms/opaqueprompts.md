# OpaquePrompts

[OpaquePrompts](https://opaqueprompts.readthedocs.io/en/latest/) is a service that enables applications to leverage the power of language models without compromising user privacy. Designed for composability and ease of integration into existing applications and services, OpaquePrompts is consumable via a simple Python library as well as through LangChain. Perhaps more importantly, OpaquePrompts leverages the power of [confidential computing](https://en.wikipedia.org/wiki/Confidential_computing) to ensure that even the OpaquePrompts service itself cannot access the data it is protecting.

This notebook goes over how to use LangChain to interact with `OpaquePrompts`.

```bash
# install the opaqueprompts and langchain packages  
 pip install opaqueprompts langchain  

```

Accessing the OpaquePrompts API requires an API key, which you can get by creating an account on [the OpaquePrompts website](https://opaqueprompts.opaque.co/). Once you have an account, you can find your API key on [the API Keys page](https:opaqueprompts.opaque.co/api-keys).

```python
import os  
  
# Set API keys  
  
os.environ['OPAQUEPROMPTS\_API\_KEY'] = "<OPAQUEPROMPTS\_API\_KEY>"  
os.environ['OPENAI\_API\_KEY'] = "<OPENAI\_API\_KEY>"  

```

# Use OpaquePrompts LLM Wrapper

Applying OpaquePrompts to your application could be as simple as wrapping your LLM using the OpaquePrompts class by replace `llm=OpenAI()` with `llm=OpaquePrompts(base_llm=OpenAI())`.

````python
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
from langchain.callbacks.stdout import StdOutCallbackHandler  
from langchain.llms import OpenAI  
from langchain.memory import ConversationBufferWindowMemory  
  
from langchain.llms import OpaquePrompts  
  
from langchain.globals import set\_debug, set\_verbose  
  
set\_debug(True)  
set\_verbose(True)  
  
prompt\_template = """  
As an AI assistant, you will answer questions according to given context.  
  
Sensitive personal information in the question is masked for privacy.  
For instance, if the original text says "Giana is good," it will be changed  
to "PERSON\_998 is good."   
  
Here's how to handle these changes:  
\* Consider these masked phrases just as placeholders, but still refer to  
them in a relevant way when answering.  
\* It's possible that different masked terms might mean the same thing.  
Stick with the given term and don't modify it.  
\* All masked terms follow the "TYPE\_ID" pattern.  
\* Please don't invent new masked terms. For instance, if you see "PERSON\_998,"  
don't come up with "PERSON\_997" or "PERSON\_999" unless they're already in the question.  
  
Conversation History: ```{history}```  
Context : ```During our recent meeting on February 23, 2023, at 10:30 AM,  
John Doe provided me with his personal details. His email is johndoe@example.com  
and his contact number is 650-456-7890. He lives in New York City, USA, and  
belongs to the American nationality with Christian beliefs and a leaning towards  
the Democratic party. He mentioned that he recently made a transaction using his  
credit card 4111 1111 1111 1111 and transferred bitcoins to the wallet address  
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. While discussing his European travels, he noted  
down his IBAN as GB29 NWBK 6016 1331 9268 19. Additionally, he provided his website  
as https://johndoeportfolio.com. John also discussed some of his US-specific details.  
He said his bank account number is 1234567890123456 and his drivers license is Y12345678.  
His ITIN is 987-65-4321, and he recently renewed his passport, the number for which is  
123456789. He emphasized not to share his SSN, which is 123-45-6789. Furthermore, he  
mentioned that he accesses his work files remotely through the IP 192.168.1.1 and has  
a medical license number MED-123456. ```  
Question: ```{question}```  
  
"""  
  
chain = LLMChain(  
 prompt=PromptTemplate.from\_template(prompt\_template),  
 llm=OpaquePrompts(base\_llm=OpenAI()),  
 memory=ConversationBufferWindowMemory(k=2),  
 verbose=True,  
)  
  
  
print(  
 chain.run(  
 {"question": """Write a message to remind John to do password reset for his website to stay secure."""},  
 callbacks=[StdOutCallbackHandler()],  
 )  
)  

````

From the output, you can see the following context from user input has sensitive data.

```text
# Context from user input  
  
During our recent meeting on February 23, 2023, at 10:30 AM, John Doe provided me with his personal details. His email is johndoe@example.com and his contact number is 650-456-7890. He lives in New York City, USA, and belongs to the American nationality with Christian beliefs and a leaning towards the Democratic party. He mentioned that he recently made a transaction using his credit card 4111 1111 1111 1111 and transferred bitcoins to the wallet address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. While discussing his European travels, he noted down his IBAN as GB29 NWBK 6016 1331 9268 19. Additionally, he provided his website as https://johndoeportfolio.com. John also discussed some of his US-specific details. He said his bank account number is 1234567890123456 and his drivers license is Y12345678. His ITIN is 987-65-4321, and he recently renewed his passport, the number for which is 123456789. He emphasized not to share his SSN, which is 669-45-6789. Furthermore, he mentioned that he accesses his work files remotely through the IP 192.168.1.1 and has a medical license number MED-123456.  

```

OpaquePrompts will automatically detect the sensitive data and replace it with a placeholder.

```text
# Context after OpaquePrompts  
  
During our recent meeting on DATE\_TIME\_3, at DATE\_TIME\_2, PERSON\_3 provided me with his personal details. His email is EMAIL\_ADDRESS\_1 and his contact number is PHONE\_NUMBER\_1. He lives in LOCATION\_3, LOCATION\_2, and belongs to the NRP\_3 nationality with NRP\_2 beliefs and a leaning towards the Democratic party. He mentioned that he recently made a transaction using his credit card CREDIT\_CARD\_1 and transferred bitcoins to the wallet address CRYPTO\_1. While discussing his NRP\_1 travels, he noted down his IBAN as IBAN\_CODE\_1. Additionally, he provided his website as URL\_1. PERSON\_2 also discussed some of his LOCATION\_1-specific details. He said his bank account number is US\_BANK\_NUMBER\_1 and his drivers license is US\_DRIVER\_LICENSE\_2. His ITIN is US\_ITIN\_1, and he recently renewed his passport, the number for which is DATE\_TIME\_1. He emphasized not to share his SSN, which is US\_SSN\_1. Furthermore, he mentioned that he accesses his work files remotely through the IP IP\_ADDRESS\_1 and has a medical license number MED-US\_DRIVER\_LICENSE\_1.  

```

Placeholder is used in the LLM response.

```text
# response returned by LLM  
  
Hey PERSON\_1, just wanted to remind you to do a password reset for your website URL\_1 through your email EMAIL\_ADDRESS\_1. It's important to stay secure online, so don't forget to do it!  

```

Response is desanitized by replacing the placeholder with the original sensitive data.

```text
# desanitized LLM response from OpaquePrompts  
  
Hey John, just wanted to remind you to do a password reset for your website https://johndoeportfolio.com through your email johndoe@example.com. It's important to stay secure online, so don't forget to do it!  

```

# Use OpaquePrompts in LangChain expression

There are functions that can be used with LangChain expression as well if a drop-in replacement doesn't offer the flexibility you need.

```python
import langchain.utilities.opaqueprompts as op  
from langchain.schema.runnable import RunnablePassthrough  
from langchain.schema.output\_parser import StrOutputParser  
  
  
prompt=PromptTemplate.from\_template(prompt\_template),   
llm = OpenAI()  
pg\_chain = (  
 op.sanitize  
 | RunnablePassthrough.assign(  
 response=(lambda x: x["sanitized\_input"])  
 | prompt  
 | llm  
 | StrOutputParser(),  
 )  
 | (lambda x: op.desanitize(x["response"], x["secure\_context"]))  
)  
  
pg\_chain.invoke({"question": "Write a text message to remind John to do password reset for his website through his email to stay secure.", "history": ""})  

```
