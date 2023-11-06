# Custom pairwise evaluator

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/comparison/custom.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

You can make your own pairwise string evaluators by inheriting from `PairwiseStringEvaluator` class and overwriting the `_evaluate_string_pairs` method (and the `_aevaluate_string_pairs` method if you want to use the evaluator asynchronously).

In this example, you will make a simple custom evaluator that just returns whether the first prediction has more whitespace tokenized 'words' than the second.

You can check out the reference docs for the [PairwiseStringEvaluator interface](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.schema.PairwiseStringEvaluator.html#langchain.evaluation.schema.PairwiseStringEvaluator) for more info.

```python
from typing import Optional, Any  
from langchain.evaluation import PairwiseStringEvaluator  
  
  
class LengthComparisonPairwiseEvaluator(PairwiseStringEvaluator):  
 """  
 Custom evaluator to compare two strings.  
 """  
  
 def \_evaluate\_string\_pairs(  
 self,  
 \*,  
 prediction: str,  
 prediction\_b: str,  
 reference: Optional[str] = None,  
 input: Optional[str] = None,  
 \*\*kwargs: Any,  
 ) -> dict:  
 score = int(len(prediction.split()) > len(prediction\_b.split()))  
 return {"score": score}  

```

```python
evaluator = LengthComparisonPairwiseEvaluator()  
  
evaluator.evaluate\_string\_pairs(  
 prediction="The quick brown fox jumped over the lazy dog.",  
 prediction\_b="The quick brown fox jumped over the dog.",  
)  

```

```text
 {'score': 1}  

```

## LLM-Based Example[​](#llm-based-example "Direct link to LLM-Based Example")

That example was simple to illustrate the API, but it wasn't very useful in practice. Below, use an LLM with some custom instructions to form a simple preference scorer similar to the built-in [PairwiseStringEvalChain](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.comparison.eval_chain.PairwiseStringEvalChain.html#langchain.evaluation.comparison.eval_chain.PairwiseStringEvalChain). We will use `ChatAnthropic` for the evaluator chain.

```python
# %pip install anthropic  
# %env ANTHROPIC\_API\_KEY=YOUR\_API\_KEY  

```

````python
from typing import Optional, Any  
from langchain.evaluation import PairwiseStringEvaluator  
from langchain.chat\_models import ChatAnthropic  
from langchain.chains import LLMChain  
  
  
class CustomPreferenceEvaluator(PairwiseStringEvaluator):  
 """  
 Custom evaluator to compare two strings using a custom LLMChain.  
 """  
  
 def \_\_init\_\_(self) -> None:  
 llm = ChatAnthropic(model="claude-2", temperature=0)  
 self.eval\_chain = LLMChain.from\_string(  
 llm,  
 """Which option is preferred? Do not take order into account. Evaluate based on accuracy and helpfulness. If neither is preferred, respond with C. Provide your reasoning, then finish with Preference: A/B/C  
  
Input: How do I get the path of the parent directory in python 3.8?  
Option A: You can use the following code:  
```python  
import os  
  
os.path.dirname(os.path.dirname(os.path.abspath(\_\_file\_\_)))  

````

Option B: You can use the following code:

```python
from pathlib import Path  
Path(\_\_file\_\_).absolute().parent  

```

Reasoning: Both options return the same result. However, since option B is more concise and easily understand, it is preferred.
Preference: B

Which option is preferred? Do not take order into account. Evaluate based on accuracy and helpfulness. If neither is preferred, respond with C. Provide your reasoning, then finish with Preference: A/B/C
Input: {input}
Option A: {prediction}
Option B: {prediction_b}
Reasoning:""",
)

```text
@property  
def requires\_input(self) -> bool:  
 return True  
  
@property  
def requires\_reference(self) -> bool:  
 return False  
  
def \_evaluate\_string\_pairs(  
 self,  
 \*,  
 prediction: str,  
 prediction\_b: str,  
 reference: Optional[str] = None,  
 input: Optional[str] = None,  
 \*\*kwargs: Any,  
) -> dict:  
 result = self.eval\_chain(  
 {  
 "input": input,  
 "prediction": prediction,  
 "prediction\_b": prediction\_b,  
 "stop": ["Which option is preferred?"],  
 },  
 \*\*kwargs,  
 )  
  
 response\_text = result["text"]  
 reasoning, preference = response\_text.split("Preference:", maxsplit=1)  
 preference = preference.strip()  
 score = 1.0 if preference == "A" else (0.0 if preference == "B" else None)  
 return {"reasoning": reasoning.strip(), "value": preference, "score": score}  

```

````text
  
  
```python  
evaluator = CustomPreferenceEvaluator()  

````

```python
evaluator.evaluate\_string\_pairs(  
 input="How do I import from a relative directory?",  
 prediction="use importlib! importlib.import\_module('.my\_package', '.')",  
 prediction\_b="from .sibling import foo",  
)  

```

```text
 {'reasoning': 'Option B is preferred over option A for importing from a relative directory, because it is more straightforward and concise.\n\nOption A uses the importlib module, which allows importing a module by specifying the full name as a string. While this works, it is less clear compared to option B.\n\nOption B directly imports from the relative path using dot notation, which clearly shows that it is a relative import. This is the recommended way to do relative imports in Python.\n\nIn summary, option B is more accurate and helpful as it uses the standard Python relative import syntax.',  
 'value': 'B',  
 'score': 0.0}  

```

```python
# Setting requires\_input to return True adds additional validation to avoid returning a grade when insufficient data is provided to the chain.  
  
try:  
 evaluator.evaluate\_string\_pairs(  
 prediction="use importlib! importlib.import\_module('.my\_package', '.')",  
 prediction\_b="from .sibling import foo",  
 )  
except ValueError as e:  
 print(e)  

```

```text
 CustomPreferenceEvaluator requires an input string.  

```

- [LLM-Based Example](#llm-based-example)
