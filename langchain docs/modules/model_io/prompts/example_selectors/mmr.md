# Select by maximal marginal relevance (MMR)

The `MaxMarginalRelevanceExampleSelector` selects examples based on a combination of which examples are most similar to the inputs, while also optimizing for diversity. It does this by finding the examples with the embeddings that have the greatest cosine similarity with the inputs, and then iteratively adding them while penalizing them for closeness to already selected examples.

```python
from langchain.prompts.example\_selector import (  
 MaxMarginalRelevanceExampleSelector,  
 SemanticSimilarityExampleSelector,  
)  
from langchain.vectorstores import FAISS  
from langchain.embeddings import OpenAIEmbeddings  
from langchain.prompts import FewShotPromptTemplate, PromptTemplate  
  
example\_prompt = PromptTemplate(  
 input\_variables=["input", "output"],  
 template="Input: {input}\nOutput: {output}",  
)  
  
# Examples of a pretend task of creating antonyms.  
examples = [  
 {"input": "happy", "output": "sad"},  
 {"input": "tall", "output": "short"},  
 {"input": "energetic", "output": "lethargic"},  
 {"input": "sunny", "output": "gloomy"},  
 {"input": "windy", "output": "calm"},  
]  

```

```python
example\_selector = MaxMarginalRelevanceExampleSelector.from\_examples(  
 # The list of examples available to select from.  
 examples,  
 # The embedding class used to produce embeddings which are used to measure semantic similarity.  
 OpenAIEmbeddings(),  
 # The VectorStore class that is used to store the embeddings and do a similarity search over.  
 FAISS,  
 # The number of examples to produce.  
 k=2,  
)  
mmr\_prompt = FewShotPromptTemplate(  
 # We provide an ExampleSelector instead of examples.  
 example\_selector=example\_selector,  
 example\_prompt=example\_prompt,  
 prefix="Give the antonym of every input",  
 suffix="Input: {adjective}\nOutput:",  
 input\_variables=["adjective"],  
)  

```

```python
# Input is a feeling, so should select the happy/sad example as the first one  
print(mmr\_prompt.format(adjective="worried"))  

```

```text
 Give the antonym of every input  
   
 Input: happy  
 Output: sad  
   
 Input: windy  
 Output: calm  
   
 Input: worried  
 Output:  

```

```python
# Let's compare this to what we would just get if we went solely off of similarity,  
# by using SemanticSimilarityExampleSelector instead of MaxMarginalRelevanceExampleSelector.  
example\_selector = SemanticSimilarityExampleSelector.from\_examples(  
 # The list of examples available to select from.  
 examples,  
 # The embedding class used to produce embeddings which are used to measure semantic similarity.  
 OpenAIEmbeddings(),  
 # The VectorStore class that is used to store the embeddings and do a similarity search over.  
 FAISS,  
 # The number of examples to produce.  
 k=2,  
)  
similar\_prompt = FewShotPromptTemplate(  
 # We provide an ExampleSelector instead of examples.  
 example\_selector=example\_selector,  
 example\_prompt=example\_prompt,  
 prefix="Give the antonym of every input",  
 suffix="Input: {adjective}\nOutput:",  
 input\_variables=["adjective"],  
)  
print(similar\_prompt.format(adjective="worried"))  

```

```text
 Give the antonym of every input  
   
 Input: happy  
 Output: sad  
   
 Input: sunny  
 Output: gloomy  
   
 Input: worried  
 Output:  

```
