# NLP Cloud

The [NLP Cloud](https://nlpcloud.io) serves high performance pre-trained or custom models for NER, sentiment-analysis, classification, summarization, paraphrasing, grammar and spelling correction, keywords and keyphrases extraction, chatbot, product description and ad generation, intent classification, text generation, image generation, blog post generation, code generation, question answering, automatic speech recognition, machine translation, language detection, semantic search, semantic similarity, tokenization, POS tagging, embeddings, and dependency parsing. It is ready for production, served through a REST API.

This example goes over how to use LangChain to interact with `NLP Cloud` [models](https://docs.nlpcloud.com/#models).

```bash
pip install nlpcloud  

```

```python
# get a token: https://docs.nlpcloud.com/#authentication  
  
from getpass import getpass  
  
NLPCLOUD\_API\_KEY = getpass()  

```

```text
 ········  

```

```python
import os  
  
os.environ["NLPCLOUD\_API\_KEY"] = NLPCLOUD\_API\_KEY  

```

```python
from langchain.llms import NLPCloud  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

```

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

```python
llm = NLPCloud()  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"  
  
llm\_chain.run(question)  

```

```text
 ' Justin Bieber was born in 1994, so the team that won the Super Bowl that year was the San Francisco 49ers.'  

```
