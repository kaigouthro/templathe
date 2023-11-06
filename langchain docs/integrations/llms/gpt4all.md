# GPT4All

[GitHub:nomic-ai/gpt4all](https://github.com/nomic-ai/gpt4all) an ecosystem of open-source chatbots trained on a massive collections of clean assistant data including code, stories and dialogue.

This example goes over how to use LangChain to interact with `GPT4All` models.

```python
%pip install gpt4all > /dev/null  

```

```text
 Note: you may need to restart the kernel to use updated packages.  

```

### Import GPT4All[​](#import-gpt4all "Direct link to Import GPT4All")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.llms import GPT4All  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  

```

### Set Up Question to pass to LLM[​](#set-up-question-to-pass-to-llm "Direct link to Set Up Question to pass to LLM")

```python
template = """Question: {question}  
  
Answer: Let's think step by step."""  
  
prompt = PromptTemplate(template=template, input\_variables=["question"])  

```

### Specify Model[​](#specify-model "Direct link to Specify Model")

To run locally, download a compatible ggml-formatted model.

The [gpt4all page](https://gpt4all.io/index.html) has a useful `Model Explorer` section:

- Select a model of interest
- Download using the UI and move the `.bin` to the `local_path` (noted below)

For more info, visit <https://github.com/nomic-ai/gpt4all>.

```python
local\_path = (  
 "./models/ggml-gpt4all-l13b-snoozy.bin" # replace with your desired local file path  
)  

```

```python
# Callbacks support token-wise streaming  
callbacks = [StreamingStdOutCallbackHandler()]  
  
# Verbose is required to pass to the callback manager  
llm = GPT4All(model=local\_path, callbacks=callbacks, verbose=True)  
  
# If you want to use a custom model add the backend parameter  
# Check https://docs.gpt4all.io/gpt4all\_python.html for supported backends  
llm = GPT4All(model=local\_path, backend="gptj", callbacks=callbacks, verbose=True)  

```

```python
llm\_chain = LLMChain(prompt=prompt, llm=llm)  

```

```python
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"  
  
llm\_chain.run(question)  

```

Justin Bieber was born on March 1, 1994. In 1994, The Cowboys won Super Bowl XXVIII.

- [Import GPT4All](#import-gpt4all)
- [Set Up Question to pass to LLM](#set-up-question-to-pass-to-llm)
- [Specify Model](#specify-model)
