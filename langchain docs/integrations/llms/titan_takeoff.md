# Titan Takeoff

`TitanML` helps businesses build and deploy better, smaller, cheaper, and faster NLP models through our training, compression, and inference optimization platform.

Our inference server, [Titan Takeoff](https://docs.titanml.co/docs/titan-takeoff/getting-started) enables deployment of LLMs locally on your hardware in a single command. Most generative model architectures are supported, such as Falcon, Llama 2, GPT2, T5 and many more.

## Installation[​](#installation "Direct link to Installation")

To get started with Iris Takeoff, all you need is to have docker and python installed on your local system. If you wish to use the server with gpu support, then you will need to install docker with cuda support.

For Mac and Windows users, make sure you have the docker daemon running! You can check this by running docker ps in your terminal. To start the daemon, open the docker desktop app.

Run the following command to install the Iris CLI that will enable you to run the takeoff server:

```python
pip install titan-iris  

```

## Choose a Model[​](#choose-a-model "Direct link to Choose a Model")

Takeoff supports many of the most powerful generative text models, such as Falcon, MPT, and Llama. See the [supported models](https://docs.titanml.co/docs/titan-takeoff/supported-models) for more information. For information about using your own models, see the [custom models](https://docs.titanml.co/docs/titan-takeoff/Advanced/custom-models).

Going forward in this demo we will be using the falcon 7B instruct model. This is a good open-source model that is trained to follow instructions, and is small enough to easily inference even on CPUs.

## Taking off[​](#taking-off "Direct link to Taking off")

Models are referred to by their model id on HuggingFace. Takeoff uses port 8000 by default, but can be configured to use another port. There is also support to use a Nvidia GPU by specifying cuda for the device flag.

To start the takeoff server, run:

```python
iris takeoff --model tiiuae/falcon-7b-instruct --device cpu  
iris takeoff --model tiiuae/falcon-7b-instruct --device cuda # Nvidia GPU required  
iris takeoff --model tiiuae/falcon-7b-instruct --device cpu --port 5000 # run on port 5000 (default: 8000)  

```

You will then be directed to a login page, where you will need to create an account to proceed.
After logging in, run the command onscreen to check whether the server is ready. When it is ready, you can start using the Takeoff integration.

To shutdown the server, run the following command. You will be presented with options on which Takeoff server to shut down, in case you have multiple running servers.

```python
iris takeoff --shutdown # shutdown the server  

```

## Inferencing your model[​](#inferencing-your-model "Direct link to Inferencing your model")

To access your LLM, use the TitanTakeoff LLM wrapper:

```python
from langchain.llms import TitanTakeoff  
  
llm = TitanTakeoff(  
 baseURL="http://localhost:8000",  
 generate\_max\_length=128,  
 temperature=1.0  
)  
  
prompt = "What is the largest planet in the solar system?"  
  
llm(prompt)  

```

No parameters are needed by default, but a baseURL that points to your desired URL where Takeoff is running can be specified and [generation parameters](https://docs.titanml.co/docs/titan-takeoff/Advanced/generation-parameters) can be supplied.

### Streaming[​](#streaming "Direct link to Streaming")

Streaming is also supported via the streaming flag:

```python
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
from langchain.callbacks.manager import CallbackManager  
  
llm = TitanTakeoff(callback\_manager=CallbackManager([StreamingStdOutCallbackHandler()]), streaming=True)  
  
prompt = "What is the capital of France?"  
  
llm(prompt)  

```

### Integration with LLMChain[​](#integration-with-llmchain "Direct link to Integration with LLMChain")

```python
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
  
llm = TitanTakeoff()  
  
template = "What is the capital of {country}"  
  
prompt = PromptTemplate(template=template, input\_variables=["country"])  
  
llm\_chain = LLMChain(llm=llm, prompt=prompt)  
  
generated = llm\_chain.run(country="Belgium")  
print(generated)  

```

- [Installation](#installation)

- [Choose a Model](#choose-a-model)

- [Taking off](#taking-off)

- [Inferencing your model](#inferencing-your-model)

  - [Streaming](#streaming)
  - [Integration with LLMChain](#integration-with-llmchain)

- [Streaming](#streaming)

- [Integration with LLMChain](#integration-with-llmchain)
