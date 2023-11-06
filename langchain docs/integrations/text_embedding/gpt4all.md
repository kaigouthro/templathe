# GPT4All

[GPT4All](https://gpt4all.io/index.html) is a free-to-use, locally running, privacy-aware chatbot. There is no GPU or internet required. It features popular models and its own models such as GPT4All Falcon, Wizard, etc.

This notebook explains how to use [GPT4All embeddings](https://docs.gpt4all.io/gpt4all_python_embedding.html#gpt4all.gpt4all.Embed4All) with LangChain.

## Install GPT4All's Python Bindings[​](#install-gpt4alls-python-bindings "Direct link to Install GPT4All's Python Bindings")

```python
%pip install gpt4all > /dev/null  

```

Note: you may need to restart the kernel to use updated packages.

```python
from langchain.embeddings import GPT4AllEmbeddings  

```

```python
gpt4all\_embd = GPT4AllEmbeddings()  

```

```text
 100%|████████████████████████| 45.5M/45.5M [00:02<00:00, 18.5MiB/s]  
  
  
 Model downloaded at: /Users/rlm/.cache/gpt4all/ggml-all-MiniLM-L6-v2-f16.bin  
  
  
 objc[45711]: Class GGMLMetalClass is implemented in both /Users/rlm/anaconda3/envs/lcn2/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libreplit-mainline-metal.dylib (0x29fe18208) and /Users/rlm/anaconda3/envs/lcn2/lib/python3.9/site-packages/gpt4all/llmodel\_DO\_NOT\_MODIFY/build/libllamamodel-mainline-metal.dylib (0x2a0244208). One of the two will be used. Which one is undefined.  

```

```python
text = "This is a test document."  

```

## Embed the Textual Data[​](#embed-the-textual-data "Direct link to Embed the Textual Data")

```python
query\_result = gpt4all\_embd.embed\_query(text)  

```

With embed_documents you can embed multiple pieces of text. You can also map these embeddings with [Nomic's Atlas](https://docs.nomic.ai/index.html) to see a visual representation of your data.

```python
doc\_result = gpt4all\_embd.embed\_documents([text])  

```

- [Install GPT4All's Python Bindings](#install-gpt4alls-python-bindings)
- [Embed the Textual Data](#embed-the-textual-data)
