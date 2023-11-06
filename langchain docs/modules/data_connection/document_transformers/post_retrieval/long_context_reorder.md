# Lost in the middle: The problem with long contexts

No matter the architecture of your model, there is a substantial performance degradation when you include 10+ retrieved documents.
In brief: When models must access relevant information in the middle of long contexts, they tend to ignore the provided documents.
See: <https://arxiv.org/abs/2307.03172>

To avoid this issue you can re-order documents after retrieval to avoid performance degradation.

```python
import os  
import chromadb  
from langchain.vectorstores import Chroma  
from langchain.embeddings import HuggingFaceEmbeddings  
from langchain.document\_transformers import (  
 LongContextReorder,  
)  
from langchain.chains import StuffDocumentsChain, LLMChain  
from langchain.prompts import PromptTemplate  
from langchain.llms import OpenAI  
  
# Get embeddings.  
embeddings = HuggingFaceEmbeddings(model\_name="all-MiniLM-L6-v2")  
  
texts = [  
 "Basquetball is a great sport.",  
 "Fly me to the moon is one of my favourite songs.",  
 "The Celtics are my favourite team.",  
 "This is a document about the Boston Celtics",  
 "I simply love going to the movies",  
 "The Boston Celtics won the game by 20 points",  
 "This is just a random text.",  
 "Elden Ring is one of the best games in the last 15 years.",  
 "L. Kornet is one of the best Celtics players.",  
 "Larry Bird was an iconic NBA player.",  
]  
  
# Create a retriever  
retriever = Chroma.from\_texts(texts, embedding=embeddings).as\_retriever(  
 search\_kwargs={"k": 10}  
)  
query = "What can you tell me about the Celtics?"  
  
# Get relevant documents ordered by relevance score  
docs = retriever.get\_relevant\_documents(query)  
docs  

```

```text
 [Document(page\_content='This is a document about the Boston Celtics', metadata={}),  
 Document(page\_content='The Celtics are my favourite team.', metadata={}),  
 Document(page\_content='L. Kornet is one of the best Celtics players.', metadata={}),  
 Document(page\_content='The Boston Celtics won the game by 20 points', metadata={}),  
 Document(page\_content='Larry Bird was an iconic NBA player.', metadata={}),  
 Document(page\_content='Elden Ring is one of the best games in the last 15 years.', metadata={}),  
 Document(page\_content='Basquetball is a great sport.', metadata={}),  
 Document(page\_content='I simply love going to the movies', metadata={}),  
 Document(page\_content='Fly me to the moon is one of my favourite songs.', metadata={}),  
 Document(page\_content='This is just a random text.', metadata={})]  

```

```python
# Reorder the documents:  
# Less relevant document will be at the middle of the list and more  
# relevant elements at beginning / end.  
reordering = LongContextReorder()  
reordered\_docs = reordering.transform\_documents(docs)  
  
# Confirm that the 4 relevant documents are at beginning and end.  
reordered\_docs  

```

```text
 [Document(page\_content='The Celtics are my favourite team.', metadata={}),  
 Document(page\_content='The Boston Celtics won the game by 20 points', metadata={}),  
 Document(page\_content='Elden Ring is one of the best games in the last 15 years.', metadata={}),  
 Document(page\_content='I simply love going to the movies', metadata={}),  
 Document(page\_content='This is just a random text.', metadata={}),  
 Document(page\_content='Fly me to the moon is one of my favourite songs.', metadata={}),  
 Document(page\_content='Basquetball is a great sport.', metadata={}),  
 Document(page\_content='Larry Bird was an iconic NBA player.', metadata={}),  
 Document(page\_content='L. Kornet is one of the best Celtics players.', metadata={}),  
 Document(page\_content='This is a document about the Boston Celtics', metadata={})]  

```

```python
# We prepare and run a custom Stuff chain with reordered docs as context.  
  
# Override prompts  
document\_prompt = PromptTemplate(  
 input\_variables=["page\_content"], template="{page\_content}"  
)  
document\_variable\_name = "context"  
llm = OpenAI()  
stuff\_prompt\_override = """Given this text extracts:  
-----  
{context}  
-----  
Please answer the following question:  
{query}"""  
prompt = PromptTemplate(  
 template=stuff\_prompt\_override, input\_variables=["context", "query"]  
)  
  
# Instantiate the chain  
llm\_chain = LLMChain(llm=llm, prompt=prompt)  
chain = StuffDocumentsChain(  
 llm\_chain=llm\_chain,  
 document\_prompt=document\_prompt,  
 document\_variable\_name=document\_variable\_name,  
)  
chain.run(input\_documents=reordered\_docs, query=query)  

```
