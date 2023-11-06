# Konko

This page covers how to run models on Konko within LangChain.

Konko API is a fully managed API designed to help application developers:

Select the right LLM(s) for their application
Prototype with various open-source and proprietary LLMs
Move to production in-line with their security, privacy, throughput, latency SLAs without infrastructure set-up or administration using Konko AI's SOC 2 compliant infrastructure

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

### First you'll need an API key[​](#first-youll-need-an-api-key "Direct link to First you'll need an API key")

You can request it by messaging [support@konko.ai](mailto:support@konko.ai)

### Install Konko AI's Python SDK[​](#install-konko-ais-python-sdk "Direct link to Install Konko AI's Python SDK")

#### 1. Enable a Python3.8+ environment[​](#1-enable-a-python38-environment "Direct link to 1. Enable a Python3.8+ environment")

#### 2. Set API Keys[​](#2-set-api-keys "Direct link to 2. Set API Keys")

##### Option 1: Set Environment Variables[​](#option-1-set-environment-variables "Direct link to Option 1: Set Environment Variables")

1. You can set environment variables for

   1. KONKO_API_KEY (Required)
   1. OPENAI_API_KEY (Optional)

1. In your current shell session, use the export command:

You can set environment variables for

1. KONKO_API_KEY (Required)
1. OPENAI_API_KEY (Optional)

In your current shell session, use the export command:

```shell
export KONKO\_API\_KEY={your\_KONKO\_API\_KEY\_here}  
export OPENAI\_API\_KEY={your\_OPENAI\_API\_KEY\_here} #Optional  

```

Alternatively, you can add the above lines directly to your shell startup script (such as .bashrc or .bash_profile for Bash shell and .zshrc for Zsh shell) to have them set automatically every time a new shell session starts.

##### Option 2: Set API Keys Programmatically[​](#option-2-set-api-keys-programmatically "Direct link to Option 2: Set API Keys Programmatically")

If you prefer to set your API keys directly within your Python script or Jupyter notebook, you can use the following commands:

```python
konko.set\_api\_key('your\_KONKO\_API\_KEY\_here')   
konko.set\_openai\_api\_key('your\_OPENAI\_API\_KEY\_here') # Optional  

```

#### 3. Install the SDK[​](#3-install-the-sdk "Direct link to 3. Install the SDK")

```shell
pip install konko  

```

#### 4. Verify Installation & Authentication[​](#4-verify-installation--authentication "Direct link to 4. Verify Installation & Authentication")

```python
#Confirm konko has installed successfully  
import konko  
#Confirm API keys from Konko and OpenAI are set properly  
konko.Model.list()  

```

## Calling a model[​](#calling-a-model "Direct link to Calling a model")

Find a model on the [Konko Introduction page](https://docs.konko.ai/docs#available-models)

For example, for this [LLama 2 model](https://docs.konko.ai/docs/meta-llama-2-13b-chat). The model id would be: `"meta-llama/Llama-2-13b-chat-hf"`

Another way to find the list of models running on the Konko instance is through this [endpoint](https://docs.konko.ai/reference/listmodels).

From here, we can initialize our model:

```python
chat\_instance = ChatKonko(max\_tokens=10, model = 'meta-llama/Llama-2-13b-chat-hf')  

```

And run it:

```python
msg = HumanMessage(content="Hi")  
chat\_response = chat\_instance([msg])  

```

- [Installation and Setup](#installation-and-setup)

  - [First you'll need an API key](#first-youll-need-an-api-key)
  - [Install Konko AI's Python SDK](#install-konko-ais-python-sdk)

- [Calling a model](#calling-a-model)

- [First you'll need an API key](#first-youll-need-an-api-key)

- [Install Konko AI's Python SDK](#install-konko-ais-python-sdk)
