# Exact Match

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/string/exact_match.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

Probably the simplest ways to evaluate an LLM or runnable's string output against a reference label is by a simple string equivalence.

This can be accessed using the `exact_match` evaluator.

```python
from langchain.evaluation import ExactMatchStringEvaluator  
  
evaluator = ExactMatchStringEvaluator()  

```

Alternatively via the loader:

```python
from langchain.evaluation import load\_evaluator  
  
evaluator = load\_evaluator("exact\_match")  

```

```python
evaluator.evaluate\_strings(  
 prediction="1 LLM.",  
 reference="2 llm",  
)  

```

```text
 {'score': 0}  

```

```python
evaluator.evaluate\_strings(  
 prediction="LangChain",  
 reference="langchain",  
)  

```

```text
 {'score': 0}  

```

## Configure the ExactMatchStringEvaluator[​](#configure-the-exactmatchstringevaluator "Direct link to Configure the ExactMatchStringEvaluator")

You can relax the "exactness" when comparing strings.

```python
evaluator = ExactMatchStringEvaluator(  
 ignore\_case=True,  
 ignore\_numbers=True,  
 ignore\_punctuation=True,  
)  
  
# Alternatively  
# evaluator = load\_evaluator("exact\_match", ignore\_case=True, ignore\_numbers=True, ignore\_punctuation=True)  

```

```python
evaluator.evaluate\_strings(  
 prediction="1 LLM.",  
 reference="2 llm",  
)  

```

```text
 {'score': 1}  

```

- [Configure the ExactMatchStringEvaluator](#configure-the-exactmatchstringevaluator)
