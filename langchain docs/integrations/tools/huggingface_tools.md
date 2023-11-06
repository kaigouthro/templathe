# HuggingFace Hub Tools

[Huggingface Tools](https://huggingface.co/docs/transformers/v4.29.0/en/custom_tools) that supporting text I/O can be
loaded directly using the `load_huggingface_tool` function.

```bash
# Requires transformers>=4.29.0 and huggingface\_hub>=0.14.1  
pip install --upgrade transformers huggingface\_hub > /dev/null  

```

```python
from langchain.agents import load\_huggingface\_tool  
  
tool = load\_huggingface\_tool("lysandre/hf-model-downloads")  
  
print(f"{tool.name}: {tool.description}")  

```

```text
 model\_download\_counter: This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub. It takes the name of the category (such as text-classification, depth-estimation, etc), and returns the name of the checkpoint  

```

```python
tool.run("text-classification")  

```

```text
 'facebook/bart-large-mnli'  

```
