# Together AI

The Together API makes it easy to fine-tune or run leading open-source models with a couple lines of code. We have integrated the world’s leading open-source models, including Llama-2, RedPajama, Falcon, Alpaca, Stable Diffusion XL, and more. Read more: <https://together.ai>

To use, you'll need an API key which you can find here:
<https://api.together.xyz/settings/api-keys>. This can be passed in as init param
`together_api_key` or set as environment variable `TOGETHER_API_KEY`.

Together API reference: <https://docs.together.ai/reference/inference>

```python
from langchain.llms import Together  
  
llm = Together(  
 model="togethercomputer/RedPajama-INCITE-7B-Base",  
 temperature=0.7,  
 max\_tokens=128,  
 top\_k=1,  
 # together\_api\_key="..."  
)  
  
input\_ = """You are a teacher with a deep knowledge of machine learning and AI. \  
You provide succinct and accurate answers. Answer the following question:   
  
What is a large language model?"""  
print(llm(input\_))  

```

```text
   
   
 A: A large language model is a neural network that is trained on a large amount of text data. It is able to generate text that is similar to the training data, and can be used for tasks such as language translation, question answering, and text summarization.  
   
 A: A large language model is a neural network that is trained on a large amount of text data. It is able to generate text that is similar to the training data, and can be used for tasks such as language translation, question answering, and text summarization.  
   
 A: A large language model is a neural network that is trained on  

```
