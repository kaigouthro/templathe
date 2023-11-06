# Huggingface TextGen Inference

[Text Generation Inference](https://github.com/huggingface/text-generation-inference) is a Rust, Python and gRPC server for text generation inference. Used in production at [HuggingFace](https://huggingface.co/) to power LLMs api-inference widgets.

This notebooks goes over how to use a self hosted LLM using `Text Generation Inference`.

To use, you should have the `text_generation` python package installed.

```python
# !pip3 install text\_generation  

```

```python
from langchain.llms import HuggingFaceTextGenInference  
  
llm = HuggingFaceTextGenInference(  
 inference\_server\_url="http://localhost:8010/",  
 max\_new\_tokens=512,  
 top\_k=10,  
 top\_p=0.95,  
 typical\_p=0.95,  
 temperature=0.01,  
 repetition\_penalty=1.03,  
)  
llm("What did foo say about bar?")  

```

### Streaming[​](#streaming "Direct link to Streaming")

```python
from langchain.llms import HuggingFaceTextGenInference  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
  
  
llm = HuggingFaceTextGenInference(  
 inference\_server\_url="http://localhost:8010/",  
 max\_new\_tokens=512,  
 top\_k=10,  
 top\_p=0.95,  
 typical\_p=0.95,  
 temperature=0.01,  
 repetition\_penalty=1.03,  
 streaming=True  
)  
llm("What did foo say about bar?", callbacks=[StreamingStdOutCallbackHandler()])  

```

- [Streaming](#streaming)
