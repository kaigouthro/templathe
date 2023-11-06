# Manifest

This notebook goes over how to use Manifest and LangChain.

For more detailed information on `manifest`, and how to use it with local huggingface models like in this example, see <https://github.com/HazyResearch/manifest>

Another example of [using Manifest with Langchain](https://github.com/HazyResearch/manifest/blob/main/examples/langchain_chatgpt.html).

```bash
pip install manifest-ml  

```

```python
from manifest import Manifest  
from langchain.llms.manifest import ManifestWrapper  

```

```python
manifest = Manifest(  
 client\_name="huggingface", client\_connection="http://127.0.0.1:5000"  
)  
print(manifest.client\_pool.get\_current\_client().get\_model\_params())  

```

```python
llm = ManifestWrapper(  
 client=manifest, llm\_kwargs={"temperature": 0.001, "max\_tokens": 256}  
)  

```

```python
# Map reduce example  
from langchain.prompts import PromptTemplate  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.chains.mapreduce import MapReduceChain  
  
  
\_prompt = """Write a concise summary of the following:  
  
  
{text}  
  
  
CONCISE SUMMARY:"""  
prompt = PromptTemplate(template=\_prompt, input\_variables=["text"])  
  
text\_splitter = CharacterTextSplitter()  
  
mp\_chain = MapReduceChain.from\_params(llm, prompt, text\_splitter)  

```

```python
with open("../../modules/state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
mp\_chain.run(state\_of\_the\_union)  

```

```text
 'President Obama delivered his annual State of the Union address on Tuesday night, laying out his priorities for the coming year. Obama said the government will provide free flu vaccines to all Americans, ending the government shutdown and allowing businesses to reopen. The president also said that the government will continue to send vaccines to 112 countries, more than any other nation. "We have lost so much to COVID-19," Trump said. "Time with one another. And worst of all, so much loss of life." He said the CDC is working on a vaccine for kids under 5, and that the government will be ready with plenty of vaccines when they are available. Obama says the new guidelines are a "great step forward" and that the virus is no longer a threat. He says the government is launching a "Test to Treat" initiative that will allow people to get tested at a pharmacy and get antiviral pills on the spot at no cost. Obama says the new guidelines are a "great step forward" and that the virus is no longer a threat. He says the government will continue to send vaccines to 112 countries, more than any other nation. "We are coming for your'  

```

## Compare HF Models[​](#compare-hf-models "Direct link to Compare HF Models")

```python
from langchain.model\_laboratory import ModelLaboratory  
  
manifest1 = ManifestWrapper(  
 client=Manifest(  
 client\_name="huggingface", client\_connection="http://127.0.0.1:5000"  
 ),  
 llm\_kwargs={"temperature": 0.01},  
)  
manifest2 = ManifestWrapper(  
 client=Manifest(  
 client\_name="huggingface", client\_connection="http://127.0.0.1:5001"  
 ),  
 llm\_kwargs={"temperature": 0.01},  
)  
manifest3 = ManifestWrapper(  
 client=Manifest(  
 client\_name="huggingface", client\_connection="http://127.0.0.1:5002"  
 ),  
 llm\_kwargs={"temperature": 0.01},  
)  
llms = [manifest1, manifest2, manifest3]  
model\_lab = ModelLaboratory(llms)  

```

```python
model\_lab.compare("What color is a flamingo?")  

```

```text
 Input:  
 What color is a flamingo?  
   
 ManifestWrapper  
 Params: {'model\_name': 'bigscience/T0\_3B', 'model\_path': 'bigscience/T0\_3B', 'temperature': 0.01}  
 pink  
   
 ManifestWrapper  
 Params: {'model\_name': 'EleutherAI/gpt-neo-125M', 'model\_path': 'EleutherAI/gpt-neo-125M', 'temperature': 0.01}  
 A flamingo is a small, round  
   
 ManifestWrapper  
 Params: {'model\_name': 'google/flan-t5-xl', 'model\_path': 'google/flan-t5-xl', 'temperature': 0.01}  
 pink  
   

```

- [Compare HF Models](#compare-hf-models)
