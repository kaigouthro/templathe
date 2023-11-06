# Regex Match

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/string/regex_match.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

To evaluate chain or runnable string predictions against a custom regex, you can use the `regex_match` evaluator.

```python
from langchain.evaluation import RegexMatchStringEvaluator  
  
evaluator = RegexMatchStringEvaluator()  

```

Alternatively via the loader:

```python
from langchain.evaluation import load\_evaluator  
  
evaluator = load\_evaluator("regex\_match")  

```

```python
# Check for the presence of a YYYY-MM-DD string.  
evaluator.evaluate\_strings(  
 prediction="The delivery will be made on 2024-01-05",  
 reference=".\*\\b\\d{4}-\\d{2}-\\d{2}\\b.\*"  
)  

```

```text
 {'score': 1}  

```

```python
# Check for the presence of a MM-DD-YYYY string.  
evaluator.evaluate\_strings(  
 prediction="The delivery will be made on 2024-01-05",  
 reference=".\*\\b\\d{2}-\\d{2}-\\d{4}\\b.\*"  
)  

```

```text
 {'score': 0}  

```

```python
# Check for the presence of a MM-DD-YYYY string.  
evaluator.evaluate\_strings(  
 prediction="The delivery will be made on 01-05-2024",  
 reference=".\*\\b\\d{2}-\\d{2}-\\d{4}\\b.\*"  
)  

```

```text
 {'score': 1}  

```

## Match against multiple patterns[​](#match-against-multiple-patterns "Direct link to Match against multiple patterns")

To match against multiple patterns, use a regex union "|".

```python
# Check for the presence of a MM-DD-YYYY string or YYYY-MM-DD  
evaluator.evaluate\_strings(  
 prediction="The delivery will be made on 01-05-2024",  
 reference="|".join([".\*\\b\\d{4}-\\d{2}-\\d{2}\\b.\*", ".\*\\b\\d{2}-\\d{2}-\\d{4}\\b.\*"])  
)  

```

```text
 {'score': 1}  

```

## Configure the RegexMatchStringEvaluator[​](#configure-the-regexmatchstringevaluator "Direct link to Configure the RegexMatchStringEvaluator")

You can specify any regex flags to use when matching.

```python
import re  
  
evaluator = RegexMatchStringEvaluator(  
 flags=re.IGNORECASE  
)  
  
# Alternatively  
# evaluator = load\_evaluator("exact\_match", flags=re.IGNORECASE)  

```

```python
evaluator.evaluate\_strings(  
 prediction="I LOVE testing",  
 reference="I love testing",  
)  

```

```text
 {'score': 1}  

```

- [Match against multiple patterns](#match-against-multiple-patterns)
- [Configure the RegexMatchStringEvaluator](#configure-the-regexmatchstringevaluator)
