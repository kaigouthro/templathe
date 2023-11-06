# Banana

Banana provided serverless GPU inference for AI models, including a CI/CD build pipeline and a simple Python framework (Potassium) to server your models.

This page covers how to use the [Banana](https://www.banana.dev) ecosystem within LangChain.

It is broken into two parts:

- installation and setup,
- and then references to specific Banana wrappers.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

- Install with `pip install banana-dev`
- Get an Banana api key from the [Banana.dev dashboard](https://app.banana.dev) and set it as an environment variable (`BANANA_API_KEY`)
- Get your model's key and url slug from the model's details page

## Define your Banana Template[​](#define-your-banana-template "Direct link to Define your Banana Template")

You'll need to set up a Github repo for your Banana app. You can get started in 5 minutes using [this guide](https://docs.banana.dev/banana-docs/).

Alternatively, for a ready-to-go LLM example, you can check out Banana's [CodeLlama-7B-Instruct-GPTQ](https://github.com/bananaml/demo-codellama-7b-instruct-gptq) GitHub repository. Just fork it and deploy it within Banana.

Other starter repos are available [here](https://github.com/orgs/bananaml/repositories?q=demo-&type=all&language=&sort=).

## Build the Banana app[​](#build-the-banana-app "Direct link to Build the Banana app")

To use Banana apps within Langchain, they must include the `outputs` key
in the returned json, and the value must be a string.

```python
# Return the results as a dictionary  
result = {'outputs': result}  

```

An example inference function would be:

````python
@app.handler("/")  
def handler(context: dict, request: Request) -> Response:  
 """Handle a request to generate code from a prompt."""  
 model = context.get("model")  
 tokenizer = context.get("tokenizer")  
 max\_new\_tokens = request.json.get("max\_new\_tokens", 512)  
 temperature = request.json.get("temperature", 0.7)  
 prompt = request.json.get("prompt")  
 prompt\_template=f'''[INST] Write code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```:  
 {prompt}  
 [/INST]  
 '''  
 input\_ids = tokenizer(prompt\_template, return\_tensors='pt').input\_ids.cuda()  
 output = model.generate(inputs=input\_ids, temperature=temperature, max\_new\_tokens=max\_new\_tokens)  
 result = tokenizer.decode(output[0])  
 return Response(json={"outputs": result}, status=200)  

````

This example is from the `app.py` file in [CodeLlama-7B-Instruct-GPTQ](https://github.com/bananaml/demo-codellama-7b-instruct-gptq).

## Wrappers[​](#wrappers "Direct link to Wrappers")

### LLM[​](#llm "Direct link to LLM")

Within Langchain, there exists a Banana LLM wrapper, which you can access with

```python
from langchain.llms import Banana  

```

You need to provide a model key and model url slug, which you can get from the model's details page in the [Banana.dev dashboard](https://app.banana.dev).

```python
llm = Banana(model\_key="YOUR\_MODEL\_KEY", model\_url\_slug="YOUR\_MODEL\_URL\_SLUG")  

```

- [Installation and Setup](#installation-and-setup)

- [Define your Banana Template](#define-your-banana-template)

- [Build the Banana app](#build-the-banana-app)

- [Wrappers](#wrappers)

  - [LLM](#llm)

- [LLM](#llm)
