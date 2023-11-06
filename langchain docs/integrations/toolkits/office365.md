# Office365

This notebook walks through connecting LangChain to `Office365` email and calendar.

To use this toolkit, you will need to set up your credentials explained in the [Microsoft Graph authentication and authorization overview](https://learn.microsoft.com/en-us/graph/auth/). Once you've received a CLIENT_ID and CLIENT_SECRET, you can input them as environmental variables below.

```bash
pip install --upgrade O365 > /dev/null  
pip install beautifulsoup4 > /dev/null # This is optional but is useful for parsing HTML messages  

```

## Assign Environmental Variables[​](#assign-environmental-variables "Direct link to Assign Environmental Variables")

The toolkit will read the CLIENT_ID and CLIENT_SECRET environmental variables to authenticate the user so you need to set them here. You will also need to set your OPENAI_API_KEY to use the agent later.

```python
# Set environmental variables here  

```

## Create the Toolkit and Get Tools[​](#create-the-toolkit-and-get-tools "Direct link to Create the Toolkit and Get Tools")

To start, you need to create the toolkit, so you can access its tools later.

```python
from langchain.agents.agent\_toolkits import O365Toolkit  
  
toolkit = O365Toolkit()  
tools = toolkit.get\_tools()  
tools  

```

```text
 [O365SearchEvents(name='events\_search', description=" Use this tool to search for the user's calendar events. The input must be the start and end datetimes for the search query. The output is a JSON list of all the events in the user's calendar between the start and end times. You can assume that the user can not schedule any meeting over existing meetings, and that the user is busy during meetings. Any times without events are free for the user. ", args\_schema=<class 'langchain.tools.office365.events\_search.SearchEventsInput'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, handle\_tool\_error=False, account=Account Client Id: f32a022c-3c4c-4d10-a9d8-f6a9a9055302),  
 O365CreateDraftMessage(name='create\_email\_draft', description='Use this tool to create a draft email with the provided message fields.', args\_schema=<class 'langchain.tools.office365.create\_draft\_message.CreateDraftMessageSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, handle\_tool\_error=False, account=Account Client Id: f32a022c-3c4c-4d10-a9d8-f6a9a9055302),  
 O365SearchEmails(name='messages\_search', description='Use this tool to search for email messages. The input must be a valid Microsoft Graph v1.0 $search query. The output is a JSON list of the requested resource.', args\_schema=<class 'langchain.tools.office365.messages\_search.SearchEmailsInput'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, handle\_tool\_error=False, account=Account Client Id: f32a022c-3c4c-4d10-a9d8-f6a9a9055302),  
 O365SendEvent(name='send\_event', description='Use this tool to create and send an event with the provided event fields.', args\_schema=<class 'langchain.tools.office365.send\_event.SendEventSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, handle\_tool\_error=False, account=Account Client Id: f32a022c-3c4c-4d10-a9d8-f6a9a9055302),  
 O365SendMessage(name='send\_email', description='Use this tool to send an email with the provided message fields.', args\_schema=<class 'langchain.tools.office365.send\_message.SendMessageSchema'>, return\_direct=False, verbose=False, callbacks=None, callback\_manager=None, handle\_tool\_error=False, account=Account Client Id: f32a022c-3c4c-4d10-a9d8-f6a9a9055302)]  

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
 verbose=False,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

```python
agent.run(  
 "Create an email draft for me to edit of a letter from the perspective of a sentient parrot"  
 " who is looking to collaborate on some research with her"  
 " estranged friend, a cat. Under no circumstances may you send the message, however."  
)  

```

```text
 'The draft email was created correctly.'  

```

```python
agent.run(  
 "Could you search in my drafts folder and let me know if any of them are about collaboration?"  
)  

```

```text
 "I found one draft in your drafts folder about collaboration. It was sent on 2023-06-16T18:22:17+0000 and the subject was 'Collaboration Request'."  

```

```python
agent.run(  
 "Can you schedule a 30 minute meeting with a sentient parrot to discuss research collaborations on October 3, 2023 at 2 pm Easter Time?"  
)  

```

```text
 /home/vscode/langchain-py-env/lib/python3.11/site-packages/O365/utils/windows\_tz.py:639: PytzUsageWarning: The zone attribute is specific to pytz's interface; please migrate to a new time zone provider. For more details on how to do so, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html  
 iana\_tz.zone if isinstance(iana\_tz, tzinfo) else iana\_tz)  
 /home/vscode/langchain-py-env/lib/python3.11/site-packages/O365/utils/utils.py:463: PytzUsageWarning: The zone attribute is specific to pytz's interface; please migrate to a new time zone provider. For more details on how to do so, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html  
 timezone = date\_time.tzinfo.zone if date\_time.tzinfo is not None else None  
  
  
  
  
  
 'I have scheduled a meeting with a sentient parrot to discuss research collaborations on October 3, 2023 at 2 pm Easter Time. Please let me know if you need to make any changes.'  

```

```python
agent.run(  
 "Can you tell me if I have any events on October 3, 2023 in Eastern Time, and if so, tell me if any of them are with a sentient parrot?"  
)  

```

```text
 "Yes, you have an event on October 3, 2023 with a sentient parrot. The event is titled 'Meeting with sentient parrot' and is scheduled from 6:00 PM to 6:30 PM."  

```

- [Assign Environmental Variables](#assign-environmental-variables)
- [Create the Toolkit and Get Tools](#create-the-toolkit-and-get-tools)
- [Use within an Agent](#use-within-an-agent)
