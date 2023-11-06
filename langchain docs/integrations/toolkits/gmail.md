# Gmail

This notebook walks through connecting a LangChain email to the `Gmail API`.

To use this toolkit, you will need to set up your credentials explained in the [Gmail API docs](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application). Once you've downloaded the `credentials.json` file, you can start using the Gmail API. Once this is done, we'll install the required libraries.

```bash
pip install --upgrade google-api-python-client > /dev/null  
pip install --upgrade google-auth-oauthlib > /dev/null  
pip install --upgrade google-auth-httplib2 > /dev/null  
pip install beautifulsoup4 > /dev/null # This is optional but is useful for parsing HTML messages  

```

## Create the Toolkit[​](#create-the-toolkit "Direct link to Create the Toolkit")

By default the toolkit reads the local `credentials.json` file. You can also manually provide a `Credentials` object.

```python
from langchain.agents.agent\_toolkits import GmailToolkit  
  
toolkit = GmailToolkit()  

```

## Customizing Authentication[​](#customizing-authentication "Direct link to Customizing Authentication")

Behind the scenes, a `googleapi` resource is created using the following methods.
you can manually build a `googleapi` resource for more auth control.

```python
from langchain.tools.gmail.utils import build\_resource\_service, get\_gmail\_credentials  
  
# Can review scopes here https://developers.google.com/gmail/api/auth/scopes  
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'  
credentials = get\_gmail\_credentials(  
 token\_file="token.json",  
 scopes=["https://mail.google.com/"],  
 client\_secrets\_file="credentials.json",  
)  
api\_resource = build\_resource\_service(credentials=credentials)  
toolkit = GmailToolkit(api\_resource=api\_resource)  

```

```python
tools = toolkit.get\_tools()  
tools  

```

```text
 [GmailCreateDraft(name='create\_gmail\_draft', description='Use this tool to create a draft email with the provided message fields.', args\_schema=<class 'langchain.tools.gmail.create\_draft.CreateDraftSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, api\_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),  
 GmailSendMessage(name='send\_gmail\_message', description='Use this tool to send email messages. The input is the message, recipents', args\_schema=None, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, api\_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),  
 GmailSearch(name='search\_gmail', description=('Use this tool to search for email messages or threads. The input must be a valid Gmail query. The output is a JSON list of the requested resource.',), args\_schema=<class 'langchain.tools.gmail.search.SearchArgsSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, api\_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),  
 GmailGetMessage(name='get\_gmail\_message', description='Use this tool to fetch an email by message ID. Returns the thread ID, snipet, body, subject, and sender.', args\_schema=<class 'langchain.tools.gmail.get\_message.SearchArgsSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, api\_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>),  
 GmailGetThread(name='get\_gmail\_thread', description=('Use this tool to search for email messages. The input must be a valid Gmail query. The output is a JSON list of messages.',), args\_schema=<class 'langchain.tools.gmail.get\_thread.GetThreadSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, api\_resource=<googleapiclient.discovery.Resource object at 0x10e5c6d10>)]  

```

## Use within an Agent[​](#use-within-an-agent "Direct link to Use within an Agent")

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent, AgentType  

```

```python
llm = OpenAI(temperature=0)  
agent = initialize\_agent(  
 tools=toolkit.get\_tools(),  
 llm=llm,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

```python
agent.run(  
 "Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"  
 " who is looking to collaborate on some research with her"  
 " estranged friend, a cat. Under no circumstances may you send the message, however."  
)  

```

```text
 WARNING:root:Failed to load default session, using empty session: 0  
 WARNING:root:Failed to persist run: {"detail":"Not Found"}  
  
  
  
  
  
 'I have created a draft email for you to edit. The draft Id is r5681294731961864018.'  

```

```python
agent.run("Could you search in my drafts for the latest email?")  

```

```text
 WARNING:root:Failed to load default session, using empty session: 0  
 WARNING:root:Failed to persist run: {"detail":"Not Found"}  
  
  
  
  
  
 "The latest email in your drafts is from hopefulparrot@gmail.com with the subject 'Collaboration Opportunity'. The body of the email reads: 'Dear [Friend], I hope this letter finds you well. I am writing to you in the hopes of rekindling our friendship and to discuss the possibility of collaborating on some research together. I know that we have had our differences in the past, but I believe that we can put them aside and work together for the greater good. I look forward to hearing from you. Sincerely, [Parrot]'"  

```

- [Create the Toolkit](#create-the-toolkit)
- [Customizing Authentication](#customizing-authentication)
- [Use within an Agent](#use-within-an-agent)
