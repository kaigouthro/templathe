# String Distance

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/string/string_distance.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

One of the simplest ways to compare an LLM or chain's string output against a reference label is by using string distance measurements such as Levenshtein or postfix distance. This can be used alongside approximate/fuzzy matching criteria for very basic unit testing.

This can be accessed using the `string_distance` evaluator, which uses distance metric's from the [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) library.

**Note:** The returned scores are *distances*, meaning lower is typically "better".

For more information, check out the reference docs for the [StringDistanceEvalChain](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.string_distance.base.StringDistanceEvalChain.html#langchain.evaluation.string_distance.base.StringDistanceEvalChain) for more info.

```python
# %pip install rapidfuzz  

```

```python
from langchain.evaluation import load\_evaluator  
  
evaluator = load\_evaluator("string\_distance")  

```

```python
evaluator.evaluate\_strings(  
 prediction="The job is completely done.",  
 reference="The job is done",  
)  

```

```text
 {'score': 0.11555555555555552}  

```

```python
# The results purely character-based, so it's less useful when negation is concerned  
evaluator.evaluate\_strings(  
 prediction="The job is done.",  
 reference="The job isn't done",  
)  

```

```text
 {'score': 0.0724999999999999}  

```

## Configure the String Distance Metric[​](#configure-the-string-distance-metric "Direct link to Configure the String Distance Metric")

By default, the `StringDistanceEvalChain` uses levenshtein distance, but it also supports other string distance algorithms. Configure using the `distance` argument.

```python
from langchain.evaluation import StringDistance  
  
list(StringDistance)  

```

```text
 [<StringDistance.DAMERAU\_LEVENSHTEIN: 'damerau\_levenshtein'>,  
 <StringDistance.LEVENSHTEIN: 'levenshtein'>,  
 <StringDistance.JARO: 'jaro'>,  
 <StringDistance.JARO\_WINKLER: 'jaro\_winkler'>]  

```

```python
jaro\_evaluator = load\_evaluator(  
 "string\_distance", distance=StringDistance.JARO  
)  

```

```python
jaro\_evaluator.evaluate\_strings(  
 prediction="The job is completely done.",  
 reference="The job is done",  
)  

```

```text
 {'score': 0.19259259259259254}  

```

```python
jaro\_evaluator.evaluate\_strings(  
 prediction="The job is done.",  
 reference="The job isn't done",  
)  

```

```text
 {'score': 0.12083333333333324}  

```

- [Configure the String Distance Metric](#configure-the-string-distance-metric)
