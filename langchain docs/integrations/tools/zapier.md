# Zapier Natural Language Actions

**Deprecated** This API will be sunset on 2023-11-17: <https://nla.zapier.com/start/>

[Zapier Natural Language Actions](https://nla.zapier.com/start/) gives you access to the 5k+ apps, 20k+ actions on Zapier's platform through a natural language API interface.

NLA supports apps like `Gmail`, `Salesforce`, `Trello`, `Slack`, `Asana`, `HubSpot`, `Google Sheets`, `Microsoft Teams`, and thousands more apps: <https://zapier.com/apps>
`Zapier NLA` handles ALL the underlying API auth and translation from natural language --> underlying API call --> return simplified output for LLMs. The key idea is you, or your users, expose a set of actions via an oauth-like setup window, which you can then query and execute via a REST API.

NLA offers both API Key and OAuth for signing NLA API requests.

1. Server-side (API Key): for quickly getting started, testing, and production scenarios where LangChain will only use actions exposed in the developer's Zapier account (and will use the developer's connected accounts on Zapier.com)
1. User-facing (Oauth): for production scenarios where you are deploying an end-user facing application and LangChain needs access to end-user's exposed actions and connected accounts on Zapier.com

Server-side (API Key): for quickly getting started, testing, and production scenarios where LangChain will only use actions exposed in the developer's Zapier account (and will use the developer's connected accounts on Zapier.com)

User-facing (Oauth): for production scenarios where you are deploying an end-user facing application and LangChain needs access to end-user's exposed actions and connected accounts on Zapier.com

This quick start focus mostly on the server-side use case for brevity. Jump to [Example Using OAuth Access Token](#oauth) to see a short example how to set up Zapier for user-facing situations. Review [full docs](https://nla.zapier.com/start/) for full user-facing oauth developer support.

This example goes over how to use the Zapier integration with a `SimpleSequentialChain`, then an `Agent`.
In code, below:

```python
import os  
  
# get from https://platform.openai.com/  
os.environ["OPENAI\_API\_KEY"] = os.environ.get("OPENAI\_API\_KEY", "")  
  
# get from https://nla.zapier.com/docs/authentication/ after logging in):  
os.environ["ZAPIER\_NLA\_API\_KEY"] = os.environ.get("ZAPIER\_NLA\_API\_KEY", "")  

```

## Example with Agent[​](#example-with-agent "Direct link to Example with Agent")

Zapier tools can be used with an agent. See the example below.

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent  
from langchain.agents.agent\_toolkits import ZapierToolkit  
from langchain.agents import AgentType  
from langchain.utilities.zapier import ZapierNLAWrapper  

```

```python
## step 0. expose gmail 'find email' and slack 'send channel message' actions  
  
# first go here, log in, expose (enable) the two actions: https://nla.zapier.com/demo/start -- for this example, can leave all fields "Have AI guess"  
# in an oauth scenario, you'd get your own <provider> id (instead of 'demo') which you route your users through first  

```

```python
llm = OpenAI(temperature=0)  
zapier = ZapierNLAWrapper()  
toolkit = ZapierToolkit.from\_zapier\_nla\_wrapper(zapier)  
agent = initialize\_agent(  
 toolkit.get\_tools(), llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  

```

```python
agent.run(  
 "Summarize the last email I received regarding Silicon Valley Bank. Send the summary to the #test-zapier channel in slack."  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
 I need to find the email and summarize it.  
 Action: Gmail: Find Email  
 Action Input: Find the latest email from Silicon Valley Bank  
 Observation: {"from\_\_name": "Silicon Valley Bridge Bank, N.A.", "from\_\_email": "sreply@svb.com", "body\_plain": "Dear Clients, After chaotic, tumultuous & stressful days, we have clarity on path for SVB, FDIC is fully insuring all deposits & have an ask for clients & partners as we rebuild. Tim Mayopoulos <https://eml.svb.com/NjEwLUtBSy0yNjYAAAGKgoxUeBCLAyF\_NxON97X4rKEaNBLG", "reply\_to\_\_email": "sreply@svb.com", "subject": "Meet the new CEO Tim Mayopoulos", "date": "Tue, 14 Mar 2023 23:42:29 -0500 (CDT)", "message\_url": "https://mail.google.com/mail/u/0/#inbox/186e393b13cfdf0a", "attachment\_count": "0", "to\_\_emails": "ankush@langchain.dev", "message\_id": "186e393b13cfdf0a", "labels": "IMPORTANT, CATEGORY\_UPDATES, INBOX"}  
 Thought: I need to summarize the email and send it to the #test-zapier channel in Slack.  
 Action: Slack: Send Channel Message  
 Action Input: Send a slack message to the #test-zapier channel with the text "Silicon Valley Bank has announced that Tim Mayopoulos is the new CEO. FDIC is fully insuring all deposits and they have an ask for clients and partners as they rebuild."  
 Observation: {"message\_\_text": "Silicon Valley Bank has announced that Tim Mayopoulos is the new CEO. FDIC is fully insuring all deposits and they have an ask for clients and partners as they rebuild.", "message\_\_permalink": "https://langchain.slack.com/archives/C04TSGU0RA7/p1678859932375259", "channel": "C04TSGU0RA7", "message\_\_bot\_profile\_\_name": "Zapier", "message\_\_team": "T04F8K3FZB5", "message\_\_bot\_id": "B04TRV4R74K", "message\_\_bot\_profile\_\_deleted": "false", "message\_\_bot\_profile\_\_app\_id": "A024R9PQM", "ts\_time": "2023-03-15T05:58:52Z", "message\_\_bot\_profile\_\_icons\_\_image\_36": "https://avatars.slack-edge.com/2022-08-02/3888649620612\_f864dc1bb794cf7d82b0\_36.png", "message\_\_blocks[]block\_id": "kdZZ", "message\_\_blocks[]elements[]type": "['rich\_text\_section']"}  
 Thought: I now know the final answer.  
 Final Answer: I have sent a summary of the last email from Silicon Valley Bank to the #test-zapier channel in Slack.  
   
 > Finished chain.  
  
  
  
  
  
 'I have sent a summary of the last email from Silicon Valley Bank to the #test-zapier channel in Slack.'  

```

## Example with SimpleSequentialChain[​](#example-with-simplesequentialchain "Direct link to Example with SimpleSequentialChain")

If you need more explicit control, use a chain, like below.

```python
from langchain.llms import OpenAI  
from langchain.chains import LLMChain, TransformChain, SimpleSequentialChain  
from langchain.prompts import PromptTemplate  
from langchain.tools.zapier.tool import ZapierNLARunAction  
from langchain.utilities.zapier import ZapierNLAWrapper  

```

```python
## step 0. expose gmail 'find email' and slack 'send direct message' actions  
  
# first go here, log in, expose (enable) the two actions: https://nla.zapier.com/demo/start -- for this example, can leave all fields "Have AI guess"  
# in an oauth scenario, you'd get your own <provider> id (instead of 'demo') which you route your users through first  
  
actions = ZapierNLAWrapper().list()  

```

```python
## step 1. gmail find email  
  
GMAIL\_SEARCH\_INSTRUCTIONS = "Grab the latest email from Silicon Valley Bank"  
  
  
def nla\_gmail(inputs):  
 action = next(  
 (a for a in actions if a["description"].startswith("Gmail: Find Email")), None  
 )  
 return {  
 "email\_data": ZapierNLARunAction(  
 action\_id=action["id"],  
 zapier\_description=action["description"],  
 params\_schema=action["params"],  
 ).run(inputs["instructions"])  
 }  
  
  
gmail\_chain = TransformChain(  
 input\_variables=["instructions"],  
 output\_variables=["email\_data"],  
 transform=nla\_gmail,  
)  

```

```python
## step 2. generate draft reply  
  
template = """You are an assisstant who drafts replies to an incoming email. Output draft reply in plain text (not JSON).  
  
Incoming email:  
{email\_data}  
  
Draft email reply:"""  
  
prompt\_template = PromptTemplate(input\_variables=["email\_data"], template=template)  
reply\_chain = LLMChain(llm=OpenAI(temperature=0.7), prompt=prompt\_template)  

```

```python
## step 3. send draft reply via a slack direct message  
  
SLACK\_HANDLE = "@Ankush Gola"  
  
  
def nla\_slack(inputs):  
 action = next(  
 (  
 a  
 for a in actions  
 if a["description"].startswith("Slack: Send Direct Message")  
 ),  
 None,  
 )  
 instructions = f'Send this to {SLACK\_HANDLE} in Slack: {inputs["draft\_reply"]}'  
 return {  
 "slack\_data": ZapierNLARunAction(  
 action\_id=action["id"],  
 zapier\_description=action["description"],  
 params\_schema=action["params"],  
 ).run(instructions)  
 }  
  
  
slack\_chain = TransformChain(  
 input\_variables=["draft\_reply"],  
 output\_variables=["slack\_data"],  
 transform=nla\_slack,  
)  

```

```python
## finally, execute  
  
overall\_chain = SimpleSequentialChain(  
 chains=[gmail\_chain, reply\_chain, slack\_chain], verbose=True  
)  
overall\_chain.run(GMAIL\_SEARCH\_INSTRUCTIONS)  

```

```text
   
   
 > Entering new SimpleSequentialChain chain...  
 {"from\_\_name": "Silicon Valley Bridge Bank, N.A.", "from\_\_email": "sreply@svb.com", "body\_plain": "Dear Clients, After chaotic, tumultuous & stressful days, we have clarity on path for SVB, FDIC is fully insuring all deposits & have an ask for clients & partners as we rebuild. Tim Mayopoulos <https://eml.svb.com/NjEwLUtBSy0yNjYAAAGKgoxUeBCLAyF\_NxON97X4rKEaNBLG", "reply\_to\_\_email": "sreply@svb.com", "subject": "Meet the new CEO Tim Mayopoulos", "date": "Tue, 14 Mar 2023 23:42:29 -0500 (CDT)", "message\_url": "https://mail.google.com/mail/u/0/#inbox/186e393b13cfdf0a", "attachment\_count": "0", "to\_\_emails": "ankush@langchain.dev", "message\_id": "186e393b13cfdf0a", "labels": "IMPORTANT, CATEGORY\_UPDATES, INBOX"}  
   
 Dear Silicon Valley Bridge Bank,   
   
 Thank you for your email and the update regarding your new CEO Tim Mayopoulos. We appreciate your dedication to keeping your clients and partners informed and we look forward to continuing our relationship with you.   
   
 Best regards,   
 [Your Name]  
 {"message\_\_text": "Dear Silicon Valley Bridge Bank, \n\nThank you for your email and the update regarding your new CEO Tim Mayopoulos. We appreciate your dedication to keeping your clients and partners informed and we look forward to continuing our relationship with you. \n\nBest regards, \n[Your Name]", "message\_\_permalink": "https://langchain.slack.com/archives/D04TKF5BBHU/p1678859968241629", "channel": "D04TKF5BBHU", "message\_\_bot\_profile\_\_name": "Zapier", "message\_\_team": "T04F8K3FZB5", "message\_\_bot\_id": "B04TRV4R74K", "message\_\_bot\_profile\_\_deleted": "false", "message\_\_bot\_profile\_\_app\_id": "A024R9PQM", "ts\_time": "2023-03-15T05:59:28Z", "message\_\_blocks[]block\_id": "p7i", "message\_\_blocks[]elements[]elements[]type": "[['text']]", "message\_\_blocks[]elements[]type": "['rich\_text\_section']"}  
   
 > Finished chain.  
  
  
  
  
  
 '{"message\_\_text": "Dear Silicon Valley Bridge Bank, \\n\\nThank you for your email and the update regarding your new CEO Tim Mayopoulos. We appreciate your dedication to keeping your clients and partners informed and we look forward to continuing our relationship with you. \\n\\nBest regards, \\n[Your Name]", "message\_\_permalink": "https://langchain.slack.com/archives/D04TKF5BBHU/p1678859968241629", "channel": "D04TKF5BBHU", "message\_\_bot\_profile\_\_name": "Zapier", "message\_\_team": "T04F8K3FZB5", "message\_\_bot\_id": "B04TRV4R74K", "message\_\_bot\_profile\_\_deleted": "false", "message\_\_bot\_profile\_\_app\_id": "A024R9PQM", "ts\_time": "2023-03-15T05:59:28Z", "message\_\_blocks[]block\_id": "p7i", "message\_\_blocks[]elements[]elements[]type": "[[\'text\']]", "message\_\_blocks[]elements[]type": "[\'rich\_text\_section\']"}'  

```

## Example Using OAuth Access Token[​](#example-using-oauth-access-token "Direct link to example-using-oauth-access-token")

The below snippet shows how to initialize the wrapper with a procured OAuth access token. Note the argument being passed in as opposed to setting an environment variable. Review the [authentication docs](https://nla.zapier.com/docs/authentication/#oauth-credentials) for full user-facing oauth developer support.

The developer is tasked with handling the OAuth handshaking to procure and refresh the access token.

```python
llm = OpenAI(temperature=0)  
zapier = ZapierNLAWrapper(zapier\_nla\_oauth\_access\_token="<fill in access token here>")  
toolkit = ZapierToolkit.from\_zapier\_nla\_wrapper(zapier)  
agent = initialize\_agent(  
 toolkit.get\_tools(), llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  
  
agent.run(  
 "Summarize the last email I received regarding Silicon Valley Bank. Send the summary to the #test-zapier channel in slack."  
)  

```

- [Example with Agent](#example-with-agent)
- [Example with SimpleSequentialChain](#example-with-simplesequentialchain)
- Example Using OAuth Access Token
