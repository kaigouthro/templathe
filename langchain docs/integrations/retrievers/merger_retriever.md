# LOTR (Merger Retriever)

`Lord of the Retrievers`, also known as `MergerRetriever`, takes a list of retrievers as input and merges the results of their get_relevant_documents() methods into a single list. The merged results will be a list of documents that are relevant to the query and that have been ranked by the different retrievers.

The `MergerRetriever` class can be used to improve the accuracy of document retrieval in a number of ways. First, it can combine the results of multiple retrievers, which can help to reduce the risk of bias in the results. Second, it can rank the results of the different retrievers, which can help to ensure that the most relevant documents are returned first.

```python
import os  
import chromadb  
from langchain.retrievers.merger\_retriever import MergerRetriever  
from langchain.vectorstores import Chroma  
from langchain.embeddings import HuggingFaceEmbeddings  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.document\_transformers import (  
 EmbeddingsRedundantFilter,  
 EmbeddingsClusteringFilter,  
)  
from langchain.retrievers.document\_compressors import DocumentCompressorPipeline  
from langchain.retrievers import ContextualCompressionRetriever  
  
# Get 3 diff embeddings.  
all\_mini = HuggingFaceEmbeddings(model\_name="all-MiniLM-L6-v2")  
multi\_qa\_mini = HuggingFaceEmbeddings(model\_name="multi-qa-MiniLM-L6-dot-v1")  
filter\_embeddings = OpenAIEmbeddings()  
  
ABS\_PATH = os.path.dirname(os.path.abspath(\_\_file\_\_))  
DB\_DIR = os.path.join(ABS\_PATH, "db")  
  
# Instantiate 2 diff cromadb indexs, each one with a diff embedding.  
client\_settings = chromadb.config.Settings(  
 is\_persistent=True,  
 persist\_directory=DB\_DIR,  
 anonymized\_telemetry=False,  
)  
db\_all = Chroma(  
 collection\_name="project\_store\_all",  
 persist\_directory=DB\_DIR,  
 client\_settings=client\_settings,  
 embedding\_function=all\_mini,  
)  
db\_multi\_qa = Chroma(  
 collection\_name="project\_store\_multi",  
 persist\_directory=DB\_DIR,  
 client\_settings=client\_settings,  
 embedding\_function=multi\_qa\_mini,  
)  
  
# Define 2 diff retrievers with 2 diff embeddings and diff search type.  
retriever\_all = db\_all.as\_retriever(  
 search\_type="similarity", search\_kwargs={"k": 5, "include\_metadata": True}  
)  
retriever\_multi\_qa = db\_multi\_qa.as\_retriever(  
 search\_type="mmr", search\_kwargs={"k": 5, "include\_metadata": True}  
)  
  
# The Lord of the Retrievers will hold the ouput of boths retrievers and can be used as any other  
# retriever on different types of chains.  
lotr = MergerRetriever(retrievers=[retriever\_all, retriever\_multi\_qa])  

```

## Remove redundant results from the merged retrievers.[​](#remove-redundant-results-from-the-merged-retrievers "Direct link to Remove redundant results from the merged retrievers.")

```python
# We can remove redundant results from both retrievers using yet another embedding.  
# Using multiples embeddings in diff steps could help reduce biases.  
filter = EmbeddingsRedundantFilter(embeddings=filter\_embeddings)  
pipeline = DocumentCompressorPipeline(transformers=[filter])  
compression\_retriever = ContextualCompressionRetriever(  
 base\_compressor=pipeline, base\_retriever=lotr  
)  

```

## Pick a representative sample of documents from the merged retrievers.[​](#pick-a-representative-sample-of-documents-from-the-merged-retrievers "Direct link to Pick a representative sample of documents from the merged retrievers.")

```python
# This filter will divide the documents vectors into clusters or "centers" of meaning.  
# Then it will pick the closest document to that center for the final results.  
# By default the result document will be ordered/grouped by clusters.  
filter\_ordered\_cluster = EmbeddingsClusteringFilter(  
 embeddings=filter\_embeddings,  
 num\_clusters=10,  
 num\_closest=1,  
)  
  
# If you want the final document to be ordered by the original retriever scores  
# you need to add the "sorted" parameter.  
filter\_ordered\_by\_retriever = EmbeddingsClusteringFilter(  
 embeddings=filter\_embeddings,  
 num\_clusters=10,  
 num\_closest=1,  
 sorted=True,  
)  
  
pipeline = DocumentCompressorPipeline(transformers=[filter\_ordered\_by\_retriever])  
compression\_retriever = ContextualCompressionRetriever(  
 base\_compressor=pipeline, base\_retriever=lotr  
)  

```

## Re-order results to avoid performance degradation.[​](#re-order-results-to-avoid-performance-degradation "Direct link to Re-order results to avoid performance degradation.")

No matter the architecture of your model, there is a sustancial performance degradation when you include 10+ retrieved documents.
In brief: When models must access relevant information in the middle of long contexts, then tend to ignore the provided documents.
See: <https://arxiv.org/abs//2307.03172>

```python
# You can use an additional document transformer to reorder documents after removing redundance.  
from langchain.document\_transformers import LongContextReorder  
  
filter = EmbeddingsRedundantFilter(embeddings=filter\_embeddings)  
reordering = LongContextReorder()  
pipeline = DocumentCompressorPipeline(transformers=[filter, reordering])  
compression\_retriever\_reordered = ContextualCompressionRetriever(  
 base\_compressor=pipeline, base\_retriever=lotr  
)  

```

- [Remove redundant results from the merged retrievers.](#remove-redundant-results-from-the-merged-retrievers)
- [Pick a representative sample of documents from the merged retrievers.](#pick-a-representative-sample-of-documents-from-the-merged-retrievers)
- [Re-order results to avoid performance degradation.](#re-order-results-to-avoid-performance-degradation)
