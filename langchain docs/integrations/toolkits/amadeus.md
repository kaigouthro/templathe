# Amadeus

This notebook walks you through connecting LangChain to the `Amadeus` travel information API

To use this toolkit, you will need to set up your credentials explained in the [Amadeus for developers getting started overview](https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335). Once you've received a AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET, you can input them as environmental variables below.

```bash
pip install --upgrade amadeus > /dev/null  

```

## Assign Environmental Variables[​](#assign-environmental-variables "Direct link to Assign Environmental Variables")

The toolkit will read the AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET environmental variables to authenticate the user so you need to set them here. You will also need to set your OPENAI_API_KEY to use the agent later.

```python
# Set environmental variables here  
import os  
  
os.environ["AMADEUS\_CLIENT\_ID"] = "CLIENT\_ID"  
os.environ["AMADEUS\_CLIENT\_SECRET"] = "CLIENT\_SECRET"  
os.environ["OPENAI\_API\_KEY"] = "API\_KEY"  

```

## Create the Amadeus Toolkit and Get Tools[​](#create-the-amadeus-toolkit-and-get-tools "Direct link to Create the Amadeus Toolkit and Get Tools")

To start, you need to create the toolkit, so you can access its tools later.

```python
from langchain.agents.agent\_toolkits.amadeus.toolkit import AmadeusToolkit  
  
toolkit = AmadeusToolkit()  
tools = toolkit.get\_tools()  

```

## Use Amadeus Toolkit within an Agent[​](#use-amadeus-toolkit-within-an-agent "Direct link to Use Amadeus Toolkit within an Agent")

```python
from langchain.llms import OpenAI  
from langchain.agents import initialize\_agent, AgentType  

```

```python
llm = OpenAI(temperature=0)  
agent = initialize\_agent(  
 tools=tools,  
 llm=llm,  
 verbose=False,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
)  

```

```python
agent.run("What is the name of the airport in Cali, Colombia?")  

```

```text
 'The closest airport to Cali, Colombia is Alfonso Bonilla Aragón International Airport (CLO).'  

```

```python
agent.run(  
 "What is the departure time of the cheapest flight on August 23, 2023 leaving Dallas, Texas before noon to Lincoln, Nebraska?"  
)  

```

```text
 'The cheapest flight on August 23, 2023 leaving Dallas, Texas before noon to Lincoln, Nebraska has a departure time of 16:42 and a total price of 276.08 EURO.'  

```

```python
agent.run(  
 "At what time does earliest flight on August 23, 2023 leaving Dallas, Texas to Lincoln, Nebraska land in Nebraska?"  
)  

```

```text
 'The earliest flight on August 23, 2023 leaving Dallas, Texas to Lincoln, Nebraska lands in Lincoln, Nebraska at 16:07.'  

```

```python
agent.run(  
 "What is the full travel time for the cheapest flight between Portland, Oregon to Dallas, TX on October 3, 2023?"  
)  

```

```text
 'The cheapest flight between Portland, Oregon to Dallas, TX on October 3, 2023 is a Spirit Airlines flight with a total price of 84.02 EURO and a total travel time of 8 hours and 43 minutes.'  

```

```python
agent.run(  
 "Please draft a concise email from Santiago to Paul, Santiago's travel agent, asking him to book the earliest flight from DFW to DCA on Aug 28, 2023. Include all flight details in the email."  
)  

```

```text
 'Dear Paul,\n\nI am writing to request that you book the earliest flight from DFW to DCA on Aug 28, 2023. The flight details are as follows:\n\nFlight 1: DFW to ATL, departing at 7:15 AM, arriving at 10:25 AM, flight number 983, carrier Delta Air Lines\nFlight 2: ATL to DCA, departing at 12:15 PM, arriving at 2:02 PM, flight number 759, carrier Delta Air Lines\n\nThank you for your help.\n\nSincerely,\nSantiago'  

```

- [Assign Environmental Variables](#assign-environmental-variables)
- [Create the Amadeus Toolkit and Get Tools](#create-the-amadeus-toolkit-and-get-tools)
- [Use Amadeus Toolkit within an Agent](#use-amadeus-toolkit-within-an-agent)
