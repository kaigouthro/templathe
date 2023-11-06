# Databricks

The [Databricks](https://www.databricks.com/) Lakehouse Platform unifies data, analytics, and AI on one platform.

This example notebook shows how to wrap Databricks endpoints as LLMs in LangChain.
It supports two endpoint types:

- Serving endpoint, recommended for production and development,
- Cluster driver proxy app, recommended for iteractive development.

```python
from langchain.llms import Databricks  

```

## Wrapping a serving endpoint[​](#wrapping-a-serving-endpoint "Direct link to Wrapping a serving endpoint")

Prerequisites:

- An LLM was registered and deployed to [a Databricks serving endpoint](https://docs.databricks.com/machine-learning/model-serving/index.html).
- You have ["Can Query" permission](https://docs.databricks.com/security/auth-authz/access-control/serving-endpoint-acl.html) to the endpoint.

The expected MLflow model signature is:

- inputs: `[{"name": "prompt", "type": "string"}, {"name": "stop", "type": "list[string]"}]`
- outputs: `[{"type": "string"}]`

If the model signature is incompatible or you want to insert extra configs, you can set `transform_input_fn` and `transform_output_fn` accordingly.

```python
# If running a Databricks notebook attached to an interactive cluster in "single user"  
# or "no isolation shared" mode, you only need to specify the endpoint name to create  
# a `Databricks` instance to query a serving endpoint in the same workspace.  
llm = Databricks(endpoint\_name="dolly")  
  
llm("How are you?")  

```

```text
 'I am happy to hear that you are in good health and as always, you are appreciated.'  

```

```python
llm("How are you?", stop=["."])  

```

```text
 'Good'  

```

```python
# Otherwise, you can manually specify the Databricks workspace hostname and personal access token  
# or set `DATABRICKS\_HOST` and `DATABRICKS\_TOKEN` environment variables, respectively.  
# See https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens  
# We strongly recommend not exposing the API token explicitly inside a notebook.  
# You can use Databricks secret manager to store your API token securely.  
# See https://docs.databricks.com/dev-tools/databricks-utils.html#secrets-utility-dbutilssecrets  
  
import os  
  
os.environ["DATABRICKS\_TOKEN"] = dbutils.secrets.get("myworkspace", "api\_token")  
  
llm = Databricks(host="myworkspace.cloud.databricks.com", endpoint\_name="dolly")  
  
llm("How are you?")  

```

```text
 'I am fine. Thank you!'  

```

```python
# If the serving endpoint accepts extra parameters like `temperature`,  
# you can set them in `model\_kwargs`.  
llm = Databricks(endpoint\_name="dolly", model\_kwargs={"temperature": 0.1})  
  
llm("How are you?")  

```

```text
 'I am fine.'  

```

```python
# Use `transform\_input\_fn` and `transform\_output\_fn` if the serving endpoint  
# expects a different input schema and does not return a JSON string,  
# respectively, or you want to apply a prompt template on top.  
  
  
def transform\_input(\*\*request):  
 full\_prompt = f"""{request["prompt"]}  
 Be Concise.  
 """  
 request["prompt"] = full\_prompt  
 return request  
  
  
llm = Databricks(endpoint\_name="dolly", transform\_input\_fn=transform\_input)  
  
llm("How are you?")  

```

```text
 'I’m Excellent. You?'  

```

## Wrapping a cluster driver proxy app[​](#wrapping-a-cluster-driver-proxy-app "Direct link to Wrapping a cluster driver proxy app")

Prerequisites:

- An LLM loaded on a Databricks interactive cluster in "single user" or "no isolation shared" mode.
- A local HTTP server running on the driver node to serve the model at `"/"` using HTTP POST with JSON input/output.
- It uses a port number between `[3000, 8000]` and listens to the driver IP address or simply `0.0.0.0` instead of localhost only.
- You have "Can Attach To" permission to the cluster.

The expected server schema (using JSON schema) is:

- inputs:

```json
{"type": "object",  
 "properties": {  
 "prompt": {"type": "string"},  
 "stop": {"type": "array", "items": {"type": "string"}}},  
 "required": ["prompt"]}  

```

- outputs: `{"type": "string"}`

```json
{"type": "object",  
 "properties": {  
 "prompt": {"type": "string"},  
 "stop": {"type": "array", "items": {"type": "string"}}},  
 "required": ["prompt"]}  

```

If the server schema is incompatible or you want to insert extra configs, you can use `transform_input_fn` and `transform_output_fn` accordingly.

The following is a minimal example for running a driver proxy app to serve an LLM:

```python
from flask import Flask, request, jsonify  
import torch  
from transformers import pipeline, AutoTokenizer, StoppingCriteria  
  
model = "databricks/dolly-v2-3b"  
tokenizer = AutoTokenizer.from\_pretrained(model, padding\_side="left")  
dolly = pipeline(model=model, tokenizer=tokenizer, trust\_remote\_code=True, device\_map="auto")  
device = dolly.device  
  
class CheckStop(StoppingCriteria):  
 def \_\_init\_\_(self, stop=None):  
 super().\_\_init\_\_()  
 self.stop = stop or []  
 self.matched = ""  
 self.stop\_ids = [tokenizer.encode(s, return\_tensors='pt').to(device) for s in self.stop]  
 def \_\_call\_\_(self, input\_ids: torch.LongTensor, scores: torch.FloatTensor, \*\*kwargs):  
 for i, s in enumerate(self.stop\_ids):  
 if torch.all((s == input\_ids[0][-s.shape[1]:])).item():  
 self.matched = self.stop[i]  
 return True  
 return False  
  
def llm(prompt, stop=None, \*\*kwargs):  
 check\_stop = CheckStop(stop)  
 result = dolly(prompt, stopping\_criteria=[check\_stop], \*\*kwargs)  
 return result[0]["generated\_text"].rstrip(check\_stop.matched)  
  
app = Flask("dolly")  
  
@app.route('/', methods=['POST'])  
def serve\_llm():  
 resp = llm(\*\*request.json)  
 return jsonify(resp)  
  
app.run(host="0.0.0.0", port="7777")  

```

Once the server is running, you can create a `Databricks` instance to wrap it as an LLM.

```python
# If running a Databricks notebook attached to the same cluster that runs the app,  
# you only need to specify the driver port to create a `Databricks` instance.  
llm = Databricks(cluster\_driver\_port="7777")  
  
llm("How are you?")  

```

```text
 'Hello, thank you for asking. It is wonderful to hear that you are well.'  

```

```python
# Otherwise, you can manually specify the cluster ID to use,  
# as well as Databricks workspace hostname and personal access token.  
  
llm = Databricks(cluster\_id="0000-000000-xxxxxxxx", cluster\_driver\_port="7777")  
  
llm("How are you?")  

```

```text
 'I am well. You?'  

```

```python
# If the app accepts extra parameters like `temperature`,  
# you can set them in `model\_kwargs`.  
llm = Databricks(cluster\_driver\_port="7777", model\_kwargs={"temperature": 0.1})  
  
llm("How are you?")  

```

```text
 'I am very well. It is a pleasure to meet you.'  

```

```python
# Use `transform\_input\_fn` and `transform\_output\_fn` if the app  
# expects a different input schema and does not return a JSON string,  
# respectively, or you want to apply a prompt template on top.  
  
  
def transform\_input(\*\*request):  
 full\_prompt = f"""{request["prompt"]}  
 Be Concise.  
 """  
 request["prompt"] = full\_prompt  
 return request  
  
  
def transform\_output(response):  
 return response.upper()  
  
  
llm = Databricks(  
 cluster\_driver\_port="7777",  
 transform\_input\_fn=transform\_input,  
 transform\_output\_fn=transform\_output,  
)  
  
llm("How are you?")  

```

```text
 'I AM DOING GREAT THANK YOU.'  

```

- [Wrapping a serving endpoint](#wrapping-a-serving-endpoint)
- [Wrapping a cluster driver proxy app](#wrapping-a-cluster-driver-proxy-app)
