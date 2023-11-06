# Custom String Evaluator

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/string/custom.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

You can make your own custom string evaluators by inheriting from the `StringEvaluator` class and implementing the `_evaluate_strings` (and `_aevaluate_strings` for async support) methods.

In this example, you will create a perplexity evaluator using the HuggingFace [evaluate](https://huggingface.co/docs/evaluate/index) library.
[Perplexity](https://en.wikipedia.org/wiki/Perplexity) is a measure of how well the generated text would be predicted by the model used to compute the metric.

```python
# %pip install evaluate > /dev/null  

```

```python
from typing import Any, Optional  
  
from langchain.evaluation import StringEvaluator  
from evaluate import load  
  
  
class PerplexityEvaluator(StringEvaluator):  
 """Evaluate the perplexity of a predicted string."""  
  
 def \_\_init\_\_(self, model\_id: str = "gpt2"):  
 self.model\_id = model\_id  
 self.metric\_fn = load(  
 "perplexity", module\_type="metric", model\_id=self.model\_id, pad\_token=0  
 )  
  
 def \_evaluate\_strings(  
 self,  
 \*,  
 prediction: str,  
 reference: Optional[str] = None,  
 input: Optional[str] = None,  
 \*\*kwargs: Any,  
 ) -> dict:  
 results = self.metric\_fn.compute(  
 predictions=[prediction], model\_id=self.model\_id  
 )  
 ppl = results["perplexities"][0]  
 return {"score": ppl}  

```

```python
evaluator = PerplexityEvaluator()  

```

```python
evaluator.evaluate\_strings(prediction="The rains in Spain fall mainly on the plain.")  

```

```text
 Using pad\_token, but it is not set yet.  
  
  
 huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...  
 To disable this warning, you can either:  
 - Avoid using `tokenizers` before the fork if possible  
 - Explicitly set the environment variable TOKENIZERS\_PARALLELISM=(true | false)  
  
  
  
 0%| | 0/1 [00:00<?, ?it/s]  
  
  
  
  
  
 {'score': 190.3675537109375}  

```

```python
# The perplexity is much higher since LangChain was introduced after 'gpt-2' was released and because it is never used in the following context.  
evaluator.evaluate\_strings(prediction="The rains in Spain fall mainly on LangChain.")  

```

```text
 Using pad\_token, but it is not set yet.  
  
  
  
 0%| | 0/1 [00:00<?, ?it/s]  
  
  
  
  
  
 {'score': 1982.0709228515625}  

```
