# Dall-E Image Generator

This notebook shows how you can generate images from a prompt synthesized using an OpenAI LLM. The images are generated using Dall-E, which uses the same OpenAI API key as the LLM.

```bash
# Needed if you would like to display images in the notebook  
pip install opencv-python scikit-image  

```

```python
from langchain.llms import OpenAI  
import os  
os.environ["OPENAI\_API\_KEY"] = "<your-key-here>"  

```

## Run as a chain[​](#run-as-a-chain "Direct link to Run as a chain")

```python
from langchain.utilities.dalle\_image\_generator import DallEAPIWrapper  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from langchain.llms import OpenAI  
  
llm = OpenAI(temperature=0.9)  
prompt = PromptTemplate(  
 input\_variables=["image\_desc"],  
 template="Generate a detailed prompt to generate an image based on the following description: {image\_desc}",  
)  
chain = LLMChain(llm=llm, prompt=prompt)  

```

```python
image\_url = DallEAPIWrapper().run(chain.run("halloween night at a haunted museum"))  

```

```python
image\_url  

```

```text
 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-i0zjYONU3PemzJ222esBaAzZ/user-f6uEIOFxoiUZivy567cDSWni/img-i7Z2ZxvJ4IbbdAiO6OXJgS3v.png?st=2023-08-11T14%3A03%3A14Z&se=2023-08-11T16%3A03%3A14Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-08-10T20%3A58%3A32Z&ske=2023-08-11T20%3A58%3A32Z&sks=b&skv=2021-08-06&sig=/sECe7C0EAq37ssgBm7g7JkVIM/Q1W3xOstd0Go6slA%3D'  

```

```python
# You can click on the link above to display the image   
# Or you can try the options below to display the image inline in this notebook  
  
try:  
 import google.colab  
 IN\_COLAB = True  
except:  
 IN\_COLAB = False  
  
if IN\_COLAB:  
 from google.colab.patches import cv2\_imshow # for image display  
 from skimage import io  
  
 image = io.imread(image\_url)   
 cv2\_imshow(image)  
else:  
 import cv2  
 from skimage import io  
  
 image = io.imread(image\_url)   
 cv2.imshow('image', image)  
 cv2.waitKey(0) #wait for a keyboard input  
 cv2.destroyAllWindows()  

```

## Run as a tool with an agent[​](#run-as-a-tool-with-an-agent "Direct link to Run as a tool with an agent")

```python
from langchain.agents import load\_tools  
from langchain.agents import initialize\_agent  
  
tools = load\_tools(['dalle-image-generator'])  
agent = initialize\_agent(tools, llm, agent="zero-shot-react-description", verbose=True)  
output = agent.run("Create an image of a halloween night at a haunted museum")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 What is the best way to turn this description into an image?  
 Action: Dall-E Image Generator  
 Action Input: A spooky Halloween night at a haunted museumhttps://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-WsxrbKyP2c8rfhCKWDyMfe8N/img-ogKfqxxOS5KWVSj4gYySR6FY.png?st=2023-01-31T07%3A38%3A25Z&se=2023-01-31T09%3A38%3A25Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-30T22%3A19%3A36Z&ske=2023-01-31T22%3A19%3A36Z&sks=b&skv=2021-08-06&sig=XsomxxBfu2CP78SzR9lrWUlbask4wBNnaMsHamy4VvU%3D  
   
 Observation: https://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-WsxrbKyP2c8rfhCKWDyMfe8N/img-ogKfqxxOS5KWVSj4gYySR6FY.png?st=2023-01-31T07%3A38%3A25Z&se=2023-01-31T09%3A38%3A25Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-30T22%3A19%3A36Z&ske=2023-01-31T22%3A19%3A36Z&sks=b&skv=2021-08-06&sig=XsomxxBfu2CP78SzR9lrWUlbask4wBNnaMsHamy4VvU%3D  
 Thought: With the image generated, I can now make my final answer.  
 Final Answer: An image of a Halloween night at a haunted museum can be seen here: https://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-WsxrbKyP2c8rfhCKWDyMfe8N/img-ogKfqxxOS5KWVSj4gYySR6FY.png?st=2023-01-31T07%3A38%3A25Z&se=2023-01-31T09%3A38%3A25Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-30T22  
   
 > Finished chain.  

```

- [Run as a chain](#run-as-a-chain)
- [Run as a tool with an agent](#run-as-a-tool-with-an-agent)
