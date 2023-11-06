# Pairwise embedding distance

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/comparison/pairwise_embedding_distance.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

One way to measure the similarity (or dissimilarity) between two predictions on a shared or similar input is to embed the predictions and compute a vector distance between the two embeddings.[\[1\]](#cite_note-1)

You can load the `pairwise_embedding_distance` evaluator to do this.

**Note:** This returns a **distance** score, meaning that the lower the number, the **more** similar the outputs are, according to their embedded representation.

Check out the reference docs for the [PairwiseEmbeddingDistanceEvalChain](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.embedding_distance.base.PairwiseEmbeddingDistanceEvalChain.html#langchain.evaluation.embedding_distance.base.PairwiseEmbeddingDistanceEvalChain) for more info.

```python
from langchain.evaluation import load\_evaluator  
  
evaluator = load\_evaluator("pairwise\_embedding\_distance")  

```

```python
evaluator.evaluate\_string\_pairs(  
 prediction="Seattle is hot in June", prediction\_b="Seattle is cool in June."  
)  

```

```text
 {'score': 0.0966466944859925}  

```

```python
evaluator.evaluate\_string\_pairs(  
 prediction="Seattle is warm in June", prediction\_b="Seattle is cool in June."  
)  

```

```text
 {'score': 0.03761174337464557}  

```

## Select the Distance Metric[​](#select-the-distance-metric "Direct link to Select the Distance Metric")

By default, the evaluator uses cosine distance. You can choose a different distance metric if you'd like.

```python
from langchain.evaluation import EmbeddingDistance  
  
list(EmbeddingDistance)  

```

```text
 [<EmbeddingDistance.COSINE: 'cosine'>,  
 <EmbeddingDistance.EUCLIDEAN: 'euclidean'>,  
 <EmbeddingDistance.MANHATTAN: 'manhattan'>,  
 <EmbeddingDistance.CHEBYSHEV: 'chebyshev'>,  
 <EmbeddingDistance.HAMMING: 'hamming'>]  

```

```python
evaluator = load\_evaluator(  
 "pairwise\_embedding\_distance", distance\_metric=EmbeddingDistance.EUCLIDEAN  
)  

```

## Select Embeddings to Use[​](#select-embeddings-to-use "Direct link to Select Embeddings to Use")

The constructor uses `OpenAI` embeddings by default, but you can configure this however you want. Below, use huggingface local embeddings

```python
from langchain.embeddings import HuggingFaceEmbeddings  
  
embedding\_model = HuggingFaceEmbeddings()  
hf\_evaluator = load\_evaluator("pairwise\_embedding\_distance", embeddings=embedding\_model)  

```

```python
hf\_evaluator.evaluate\_string\_pairs(  
 prediction="Seattle is hot in June", prediction\_b="Seattle is cool in June."  
)  

```

```text
 {'score': 0.5486443280477362}  

```

```python
hf\_evaluator.evaluate\_string\_pairs(  
 prediction="Seattle is warm in June", prediction\_b="Seattle is cool in June."  
)  

```

```text
 {'score': 0.21018880025138598}  

```

- [Select the Distance Metric](#select-the-distance-metric)
- [Select Embeddings to Use](#select-embeddings-to-use)
