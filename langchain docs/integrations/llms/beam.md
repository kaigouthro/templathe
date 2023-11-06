# Beam

Calls the Beam API wrapper to deploy and make subsequent calls to an instance of the gpt2 LLM in a cloud deployment. Requires installation of the Beam library and registration of Beam Client ID and Client Secret. By calling the wrapper an instance of the model is created and run, with returned text relating to the prompt. Additional calls can then be made by directly calling the Beam API.

[Create an account](https://www.beam.cloud/), if you don't have one already. Grab your API keys from the [dashboard](https://www.beam.cloud/dashboard/settings/api-keys).

Install the Beam CLI

```bash
curl https://raw.githubusercontent.com/slai-labs/get-beam/main/get-beam.sh -sSfL | sh  

```

Register API Keys and set your beam client id and secret environment variables:

```bash
import os  
import subprocess  
  
beam\_client\_id = "<Your beam client id>"  
beam\_client\_secret = "<Your beam client secret>"  
  
# Set the environment variables  
os.environ["BEAM\_CLIENT\_ID"] = beam\_client\_id  
os.environ["BEAM\_CLIENT\_SECRET"] = beam\_client\_secret  
  
# Run the beam configure command  
beam configure --clientId={beam\_client\_id} --clientSecret={beam\_client\_secret}  

```

Install the Beam SDK:

```bash
pip install beam-sdk  

```

**Deploy and call Beam directly from langchain!**

Note that a cold start might take a couple of minutes to return the response, but subsequent calls will be faster!

```python
from langchain.llms.beam import Beam  
  
llm = Beam(  
 model\_name="gpt2",  
 name="langchain-gpt2-test",  
 cpu=8,  
 memory="32Gi",  
 gpu="A10G",  
 python\_version="python3.8",  
 python\_packages=[  
 "diffusers[torch]>=0.10",  
 "transformers",  
 "torch",  
 "pillow",  
 "accelerate",  
 "safetensors",  
 "xformers",  
 ],  
 max\_length="50",  
 verbose=False,  
)  
  
llm.\_deploy()  
  
response = llm.\_call("Running machine learning on a remote GPU")  
  
print(response)  

```
