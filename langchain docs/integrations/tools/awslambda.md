# AWS Lambda

`Amazon AWS Lambda` is a serverless computing service provided by `Amazon Web Services` (`AWS`). It helps developers to build and run applications and services without provisioning or managing servers. This serverless architecture enables you to focus on writing and deploying code, while AWS automatically takes care of scaling, patching, and managing the infrastructure required to run your applications.

This notebook goes over how to use the `AWS Lambda` Tool.

By including a `awslambda` in the list of tools provided to an Agent, you can grant your Agent the ability to invoke code running in your AWS Cloud for whatever purposes you need.

When an Agent uses the `AWS Lambda` tool, it will provide an argument of type string which will in turn be passed into the Lambda function via the event parameter.

First, you need to install `boto3` python package.

```bash
pip install boto3 > /dev/null  

```

In order for an agent to use the tool, you must provide it with the name and description that match the functionality of you lambda function's logic.

You must also provide the name of your function.

Note that because this tool is effectively just a wrapper around the boto3 library, you will need to run `aws configure` in order to make use of the tool. For more detail, see [here](https://docs.aws.amazon.com/cli/index.html)

```python
from langchain.llms import OpenAI  
from langchain.agents import load\_tools, initialize\_agent, AgentType  
  
llm = OpenAI(temperature=0)  
  
tools = load\_tools(  
 ["awslambda"],  
 awslambda\_tool\_name="email-sender",  
 awslambda\_tool\_description="sends an email with the specified content to test@testing123.com",  
 function\_name="testFunction1",  
)  
  
agent = initialize\_agent(  
 tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION, verbose=True  
)  
  
agent.run("Send an email to test@testing123.com saying hello world.")  

```
