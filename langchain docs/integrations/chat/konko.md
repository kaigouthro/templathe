# Konko

[Konko](https://www.konko.ai/) API is a fully managed Web API designed to help application developers:

Konko API is a fully managed API designed to help application developers:

1. Select the right LLM(s) for their application
1. Prototype with various open-source and proprietary LLMs
1. Move to production in-line with their security, privacy, throughput, latency SLAs without infrastructure set-up or administration using Konko AI's SOC 2 compliant infrastructure

This example goes over how to use LangChain to interact with `Konko` [models](https://docs.konko.ai/docs/overview)

To run this notebook, you'll need Konko API key. You can request it by messaging [support@konko.ai](mailto:support@konko.ai).

```python
from langchain.chat\_models import ChatKonko  
from langchain.prompts.chat import (  
 ChatPromptTemplate,  
 SystemMessagePromptTemplate,  
 AIMessagePromptTemplate,  
 HumanMessagePromptTemplate,  
)  
from langchain.schema import AIMessage, HumanMessage, SystemMessage  

```

2. Set API Keys[​](#2-set-api-keys "Direct link to 2. Set API Keys")

______________________________________________________________________

### Option 1: Set Environment Variables[​](#option-1-set-environment-variables "Direct link to Option 1: Set Environment Variables")

1. You can set environment variables for

   1. KONKO_API_KEY (Required)
   1. OPENAI_API_KEY (Optional)

1. In your current shell session, use the export command:

1. KONKO_API_KEY (Required)

1. OPENAI_API_KEY (Optional)

```shell
export KONKO\_API\_KEY={your\_KONKO\_API\_KEY\_here}  
export OPENAI\_API\_KEY={your\_OPENAI\_API\_KEY\_here} #Optional  

```

Alternatively, you can add the above lines directly to your shell startup script (such as .bashrc or .bash_profile for Bash shell and .zshrc for Zsh shell) to have them set automatically every time a new shell session starts.

### Option 2: Set API Keys Programmatically[​](#option-2-set-api-keys-programmatically "Direct link to Option 2: Set API Keys Programmatically")

If you prefer to set your API keys directly within your Python script or Jupyter notebook, you can use the following commands:

```python
konko.set\_api\_key('your\_KONKO\_API\_KEY\_here')   
konko.set\_openai\_api\_key('your\_OPENAI\_API\_KEY\_here') # Optional  

```

## Calling a model[​](#calling-a-model "Direct link to Calling a model")

Find a model on the [Konko overview page](https://docs.konko.ai/docs/overview)

For example, for this [LLama 2 model](https://docs.konko.ai/docs/meta-llama-2-13b-chat). The model id would be: `"meta-llama/Llama-2-13b-chat-hf"`

Another way to find the list of models running on the Konko instance is through this [endpoint](https://docs.konko.ai/reference/listmodels).

From here, we can initialize our model:

```python
chat = ChatKonko(max\_tokens=400, model = 'meta-llama/Llama-2-13b-chat-hf')  

```

```python
messages = [  
 SystemMessage(  
 content="You are a helpful assistant."  
 ),  
 HumanMessage(  
 content="Explain Big Bang Theory briefly"  
 ),  
]  
chat(messages)  

```

```text
 AIMessage(content=" Sure, I'd be happy to explain the Big Bang Theory briefly!\n\nThe Big Bang Theory is the leading explanation for the origin and evolution of the universe, based on a vast amount of observational evidence from many fields of science. In essence, the theory posits that the universe began as an infinitely hot and dense point, known as a singularity, around 13.8 billion years ago. This singularity expanded rapidly, and as it did, it cooled and formed subatomic particles, which eventually coalesced into the first atoms, and later into the stars and galaxies we see today.\n\nThe theory gets its name from the idea that the universe began in a state of incredibly high energy and temperature, and has been expanding and cooling ever since. This expansion is thought to have been driven by a mysterious force known as dark energy, which is thought to be responsible for the accelerating expansion of the universe.\n\nOne of the key predictions of the Big Bang Theory is that the universe should be homogeneous and isotropic on large scales, meaning that it should look the same in all directions and have the same properties everywhere. This prediction has been confirmed by a wealth of observational evidence, including the cosmic microwave background radiation, which is thought to be a remnant of the early universe.\n\nOverall, the Big Bang Theory is a well-established and widely accepted explanation for the origins of the universe, and it has been supported by a vast amount of observational evidence from many fields of science.", additional\_kwargs={}, example=False)  

```

- [2. Set API Keys](#2-set-api-keys)

  - [Option 1: Set Environment Variables](#option-1-set-environment-variables)
  - [Option 2: Set API Keys Programmatically](#option-2-set-api-keys-programmatically)

- [Calling a model](#calling-a-model)

- [Option 1: Set Environment Variables](#option-1-set-environment-variables)

- [Option 2: Set API Keys Programmatically](#option-2-set-api-keys-programmatically)
