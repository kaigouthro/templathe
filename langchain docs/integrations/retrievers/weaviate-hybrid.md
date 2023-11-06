# Weaviate Hybrid Search

[Weaviate](https://weaviate.io/developers/weaviate) is an open-source vector database.

[Hybrid search](https://weaviate.io/blog/hybrid-search-explained) is a technique that combines multiple search algorithms to improve the accuracy and relevance of search results. It uses the best features of both keyword-based search algorithms with vector search techniques.

The `Hybrid search in Weaviate` uses sparse and dense vectors to represent the meaning and context of search queries and documents.

This notebook shows how to use `Weaviate hybrid search` as a LangChain retriever.

Set up the retriever:

```python
#!pip install weaviate-client  

```

```python
import weaviate  
import os  
  
WEAVIATE\_URL = os.getenv("WEAVIATE\_URL")  
auth\_client\_secret = (weaviate.AuthApiKey(api\_key=os.getenv("WEAVIATE\_API\_KEY")),)  
client = weaviate.Client(  
 url=WEAVIATE\_URL,  
 additional\_headers={  
 "X-Openai-Api-Key": os.getenv("OPENAI\_API\_KEY"),  
 },  
)  
  
# client.schema.delete\_all()  

```

```python
from langchain.retrievers.weaviate\_hybrid\_search import WeaviateHybridSearchRetriever  
from langchain.schema import Document  

```

```text
   

```

```python
retriever = WeaviateHybridSearchRetriever(  
 client=client,  
 index\_name="LangChain",  
 text\_key="text",  
 attributes=[],  
 create\_schema\_if\_missing=True,  
)  

```

Add some data:

```python
docs = [  
 Document(  
 metadata={  
 "title": "Embracing The Future: AI Unveiled",  
 "author": "Dr. Rebecca Simmons",  
 },  
 page\_content="A comprehensive analysis of the evolution of artificial intelligence, from its inception to its future prospects. Dr. Simmons covers ethical considerations, potentials, and threats posed by AI.",  
 ),  
 Document(  
 metadata={  
 "title": "Symbiosis: Harmonizing Humans and AI",  
 "author": "Prof. Jonathan K. Sterling",  
 },  
 page\_content="Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.",  
 ),  
 Document(  
 metadata={"title": "AI: The Ethical Quandary", "author": "Dr. Rebecca Simmons"},  
 page\_content="In her second book, Dr. Simmons delves deeper into the ethical considerations surrounding AI development and deployment. It is an eye-opening examination of the dilemmas faced by developers, policymakers, and society at large.",  
 ),  
 Document(  
 metadata={  
 "title": "Conscious Constructs: The Search for AI Sentience",  
 "author": "Dr. Samuel Cortez",  
 },  
 page\_content="Dr. Cortez takes readers on a journey exploring the controversial topic of AI consciousness. The book provides compelling arguments for and against the possibility of true AI sentience.",  
 ),  
 Document(  
 metadata={  
 "title": "Invisible Routines: Hidden AI in Everyday Life",  
 "author": "Prof. Jonathan K. Sterling",  
 },  
 page\_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.",  
 ),  
]  

```

```python
retriever.add\_documents(docs)  

```

```text
 ['3a27b0a5-8dbb-4fee-9eba-8b6bc2c252be',  
 'eeb9fd9b-a3ac-4d60-a55b-a63a25d3b907',  
 '7ebbdae7-1061-445f-a046-1989f2343d8f',  
 'c2ab315b-3cab-467f-b23a-b26ed186318d',  
 'b83765f2-e5d2-471f-8c02-c3350ade4c4f']  

```

Do a hybrid search:

```python
retriever.get\_relevant\_documents("the ethical implications of AI")  

```

```text
 [Document(page\_content='In her second book, Dr. Simmons delves deeper into the ethical considerations surrounding AI development and deployment. It is an eye-opening examination of the dilemmas faced by developers, policymakers, and society at large.', metadata={}),  
 Document(page\_content='A comprehensive analysis of the evolution of artificial intelligence, from its inception to its future prospects. Dr. Simmons covers ethical considerations, potentials, and threats posed by AI.', metadata={}),  
 Document(page\_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.", metadata={}),  
 Document(page\_content='Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.', metadata={})]  

```

Do a hybrid search with where filter:

```python
retriever.get\_relevant\_documents(  
 "AI integration in society",  
 where\_filter={  
 "path": ["author"],  
 "operator": "Equal",  
 "valueString": "Prof. Jonathan K. Sterling",  
 },  
)  

```

```text
 [Document(page\_content='Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.', metadata={}),  
 Document(page\_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.", metadata={})]  

```

Do a hybrid search with scores:

```python
retriever.get\_relevant\_documents(  
 "AI integration in society",  
 score=True,  
)  

```

```text
 [Document(page\_content='Prof. Sterling explores the potential for harmonious coexistence between humans and artificial intelligence. The book discusses how AI can be integrated into society in a beneficial and non-disruptive manner.', metadata={'\_additional': {'explainScore': '(bm25)\n(hybrid) Document eeb9fd9b-a3ac-4d60-a55b-a63a25d3b907 contributed 0.00819672131147541 to the score\n(hybrid) Document eeb9fd9b-a3ac-4d60-a55b-a63a25d3b907 contributed 0.00819672131147541 to the score', 'score': '0.016393442'}}),  
 Document(page\_content="In his follow-up to 'Symbiosis', Prof. Sterling takes a look at the subtle, unnoticed presence and influence of AI in our everyday lives. It reveals how AI has become woven into our routines, often without our explicit realization.", metadata={'\_additional': {'explainScore': '(bm25)\n(hybrid) Document b83765f2-e5d2-471f-8c02-c3350ade4c4f contributed 0.0078125 to the score\n(hybrid) Document b83765f2-e5d2-471f-8c02-c3350ade4c4f contributed 0.008064516129032258 to the score', 'score': '0.015877016'}}),  
 Document(page\_content='In her second book, Dr. Simmons delves deeper into the ethical considerations surrounding AI development and deployment. It is an eye-opening examination of the dilemmas faced by developers, policymakers, and society at large.', metadata={'\_additional': {'explainScore': '(bm25)\n(hybrid) Document 7ebbdae7-1061-445f-a046-1989f2343d8f contributed 0.008064516129032258 to the score\n(hybrid) Document 7ebbdae7-1061-445f-a046-1989f2343d8f contributed 0.0078125 to the score', 'score': '0.015877016'}}),  
 Document(page\_content='A comprehensive analysis of the evolution of artificial intelligence, from its inception to its future prospects. Dr. Simmons covers ethical considerations, potentials, and threats posed by AI.', metadata={'\_additional': {'explainScore': '(vector) [-0.0071824766 -0.0006682752 0.001723625 -0.01897258 -0.0045127636 0.0024410256 -0.020503938 0.013768672 0.009520169 -0.037972264]... \n(hybrid) Document 3a27b0a5-8dbb-4fee-9eba-8b6bc2c252be contributed 0.007936507936507936 to the score', 'score': '0.007936508'}})]  

```
