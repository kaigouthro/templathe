# AINetwork

[AI Network](https://www.ainetwork.ai/build-on-ain) is a layer 1 blockchain designed to accommodate large-scale AI models, utilizing a decentralized GPU network powered by the [$AIN token](https://www.ainetwork.ai/token), enriching AI-driven `NFTs` (`AINFTs`).

The `AINetwork Toolkit` is a set of tools for interacting with the [AINetwork Blockchain](https://www.ainetwork.ai/public/whitepaper.pdf). These tools allow you to transfer `AIN`, read and write values, create apps, and set permissions for specific paths within the blockchain database.

## Installing dependencies[​](#installing-dependencies "Direct link to Installing dependencies")

Before using the AINetwork Toolkit, you need to install the ain-py package. You can install it with pip:

```bash
pip install ain-py  

```

## Set environmental variables[​](#set-environmental-variables "Direct link to Set environmental variables")

You need to set the `AIN_BLOCKCHAIN_ACCOUNT_PRIVATE_KEY` environmental variable to your AIN Blockchain Account Private Key.

```python
import os  
  
os.environ["AIN\_BLOCKCHAIN\_ACCOUNT\_PRIVATE\_KEY"] = ""  

```

### Get AIN Blockchain private key[​](#get-ain-blockchain-private-key "Direct link to Get AIN Blockchain private key")

```python
import os  
  
from ain.account import Account  
  
if os.environ.get("AIN\_BLOCKCHAIN\_ACCOUNT\_PRIVATE\_KEY", None):  
 account = Account(os.environ["AIN\_BLOCKCHAIN\_ACCOUNT\_PRIVATE\_KEY"])  
else:  
 account = Account.create()  
 os.environ["AIN\_BLOCKCHAIN\_ACCOUNT\_PRIVATE\_KEY"] = account.private\_key  
 print(  
 f"""  
address: {account.address}  
private\_key: {account.private\_key}  
"""  
 )  
# IMPORTANT: If you plan to use this account in the future, make sure to save the  
# private key in a secure place. Losing access to your private key means losing  
# access to your account.  

```

```text
   
 address: 0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac  
 private\_key: f5e2f359bb6b7836a2ac70815473d1a290c517f847d096f5effe818de8c2cf14  
   

```

## Initialize the AINetwork Toolkit[​](#initialize-the-ainetwork-toolkit "Direct link to Initialize the AINetwork Toolkit")

You can initialize the AINetwork Toolkit like this:

```python
from langchain.agents.agent\_toolkits.ainetwork.toolkit import AINetworkToolkit  
  
toolkit = AINetworkToolkit()  
tools = toolkit.get\_tools()  
address = tools[0].interface.wallet.defaultAccount.address  

```

## Initialize the Agent with the AINetwork Toolkit[​](#initialize-the-agent-with-the-ainetwork-toolkit "Direct link to Initialize the Agent with the AINetwork Toolkit")

You can initialize the agent with the AINetwork Toolkit like this:

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.agents import initialize\_agent, AgentType  
  
llm = ChatOpenAI(temperature=0)  
agent = initialize\_agent(  
 tools=tools,  
 llm=llm,  
 verbose=True,  
 agent=AgentType.OPENAI\_FUNCTIONS,  
)  

```

## Example Usage[​](#example-usage "Direct link to Example Usage")

Here are some examples of how you can use the agent with the AINetwork Toolkit:

### Define App name to test[​](#define-app-name-to-test "Direct link to Define App name to test")

```python
appName = f"langchain\_demo\_{address.lower()}"  

```

### Create an app in the AINetwork Blockchain database[​](#create-an-app-in-the-ainetwork-blockchain-database "Direct link to Create an app in the AINetwork Blockchain database")

```python
print(  
 agent.run(  
 f"Create an app in the AINetwork Blockchain database with the name {appName}"  
 )  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINappOps` with `{'type': 'SET\_ADMIN', 'appName': 'langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac'}`  
   
   
 {"tx\_hash": "0x018846d6a9fc111edb1a2246ae2484ef05573bd2c584f3d0da155fa4b4936a9e", "result": {"gas\_amount\_total": {"bandwidth": {"service": 4002, "app": {"langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac": 2}}, "state": {"service": 1640}}, "gas\_cost\_total": 0, "func\_results": {"\_createApp": {"op\_results": {"0": {"path": "/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac", "result": {"code": 0, "bandwidth\_gas\_amount": 1}}, "1": {"path": "/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac", "result": {"code": 0, "bandwidth\_gas\_amount": 1}}, "2": {"path": "/manage\_app/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/config/admin", "result": {"code": 0, "bandwidth\_gas\_amount": 1}}}, "code": 0, "bandwidth\_gas\_amount": 2000}}, "code": 0, "bandwidth\_gas\_amount": 2001, "gas\_amount\_charged": 5642}}The app with the name "langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac" has been created in the AINetwork Blockchain database.  
   
 > Finished chain.  
 The app with the name "langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac" has been created in the AINetwork Blockchain database.  

```

### Set a value at a given path in the AINetwork Blockchain database[​](#set-a-value-at-a-given-path-in-the-ainetwork-blockchain-database "Direct link to Set a value at a given path in the AINetwork Blockchain database")

```python
print(  
 agent.run(f"Set the value {{1: 2, '34': 56}} at the path /apps/{appName}/object .")  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINvalueOps` with `{'type': 'SET', 'path': '/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/object', 'value': {'1': 2, '34': 56}}`  
   
   
 {"tx\_hash": "0x3d1a16d9808830088cdf4d37f90f4b1fa1242e2d5f6f983829064f45107b5279", "result": {"gas\_amount\_total": {"bandwidth": {"service": 0, "app": {"langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac": 1}}, "state": {"service": 0, "app": {"langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac": 674}}}, "gas\_cost\_total": 0, "code": 0, "bandwidth\_gas\_amount": 1, "gas\_amount\_charged": 0}}The value {1: 2, '34': 56} has been set at the path /apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/object.  
   
 > Finished chain.  
 The value {1: 2, '34': 56} has been set at the path /apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/object.  

```

### Set permissions for a path in the AINetwork Blockchain database[​](#set-permissions-for-a-path-in-the-ainetwork-blockchain-database "Direct link to Set permissions for a path in the AINetwork Blockchain database")

```python
print(  
 agent.run(  
 f"Set the write permissions for the path /apps/{appName}/user/$from with the"  
 " eval string auth.addr===$from ."  
 )  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINruleOps` with `{'type': 'SET', 'path': '/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/user/$from', 'eval': 'auth.addr===$from'}`  
   
   
 {"tx\_hash": "0x37d5264e580f6a217a347059a735bfa9eb5aad85ff28a95531c6dc09252664d2", "result": {"gas\_amount\_total": {"bandwidth": {"service": 0, "app": {"langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac": 1}}, "state": {"service": 0, "app": {"langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac": 712}}}, "gas\_cost\_total": 0, "code": 0, "bandwidth\_gas\_amount": 1, "gas\_amount\_charged": 0}}The write permissions for the path `/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/user/$from` have been set with the eval string `auth.addr===$from`.  
   
 > Finished chain.  
 The write permissions for the path `/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac/user/$from` have been set with the eval string `auth.addr===$from`.  

```

### Retrieve the permissions for a path in the AINetwork Blockchain database[​](#retrieve-the-permissions-for-a-path-in-the-ainetwork-blockchain-database "Direct link to Retrieve the permissions for a path in the AINetwork Blockchain database")

```python
print(agent.run(f"Retrieve the permissions for the path /apps/{appName}."))  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINownerOps` with `{'type': 'GET', 'path': '/apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac'}`  
   
   
 {".owner": {"owners": {"0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac": {"branch\_owner": true, "write\_function": true, "write\_owner": true, "write\_rule": true}}}}The permissions for the path /apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac are as follows:  
   
 - Address: 0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac  
 - branch\_owner: true  
 - write\_function: true  
 - write\_owner: true  
 - write\_rule: true  
   
 > Finished chain.  
 The permissions for the path /apps/langchain\_demo\_0x5beb4defa2ccc274498416fd7cb34235dbc122ac are as follows:  
   
 - Address: 0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac  
 - branch\_owner: true  
 - write\_function: true  
 - write\_owner: true  
 - write\_rule: true  

```

### Get AIN from faucet[​](#get-ain-from-faucet "Direct link to Get AIN from faucet")

```bash
curl http://faucet.ainetwork.ai/api/test/{address}/  

```

```text
 {"result":"0x0eb07b67b7d0a702cb60e865d3deafff3070d8508077ef793d69d6819fd92ea3","time":1692348112376}  

```

### Get AIN Balance[​](#get-ain-balance "Direct link to Get AIN Balance")

```python
print(agent.run(f"Check AIN balance of {address}"))  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINvalueOps` with `{'type': 'GET', 'path': '/accounts/0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac/balance'}`  
   
   
 100The AIN balance of address 0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac is 100 AIN.  
   
 > Finished chain.  
 The AIN balance of address 0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac is 100 AIN.  

```

### Transfer AIN[​](#transfer-ain "Direct link to Transfer AIN")

```python
print(  
 agent.run(  
 "Transfer 100 AIN to the address 0x19937b227b1b13f29e7ab18676a89ea3bdea9c5b"  
 )  
)  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `AINtransfer` with `{'address': '0x19937b227b1b13f29e7ab18676a89ea3bdea9c5b', 'amount': 100}`  
   
   
 {"tx\_hash": "0xa59d15d23373bcc00e413ac8ba18cb016bb3bdd54058d62606aec688c6ad3d2e", "result": {"gas\_amount\_total": {"bandwidth": {"service": 3}, "state": {"service": 866}}, "gas\_cost\_total": 0, "func\_results": {"\_transfer": {"op\_results": {"0": {"path": "/accounts/0x5BEB4Defa2ccc274498416Fd7Cb34235DbC122Ac/balance", "result": {"code": 0, "bandwidth\_gas\_amount": 1}}, "1": {"path": "/accounts/0x19937B227b1b13f29e7AB18676a89EA3BDEA9C5b/balance", "result": {"code": 0, "bandwidth\_gas\_amount": 1}}}, "code": 0, "bandwidth\_gas\_amount": 0}}, "code": 0, "bandwidth\_gas\_amount": 1, "gas\_amount\_charged": 869}}The transfer of 100 AIN to the address 0x19937b227b1b13f29e7ab18676a89ea3bdea9c5b was successful. The transaction hash is 0xa59d15d23373bcc00e413ac8ba18cb016bb3bdd54058d62606aec688c6ad3d2e.  
   
 > Finished chain.  
 The transfer of 100 AIN to the address 0x19937b227b1b13f29e7ab18676a89ea3bdea9c5b was successful. The transaction hash is 0xa59d15d23373bcc00e413ac8ba18cb016bb3bdd54058d62606aec688c6ad3d2e.  

```

- [Installing dependencies](#installing-dependencies)

- [Set environmental variables](#set-environmental-variables)

  - [Get AIN Blockchain private key](#get-ain-blockchain-private-key)

- [Initialize the AINetwork Toolkit](#initialize-the-ainetwork-toolkit)

- [Initialize the Agent with the AINetwork Toolkit](#initialize-the-agent-with-the-ainetwork-toolkit)

- [Example Usage](#example-usage)

  - [Define App name to test](#define-app-name-to-test)
  - [Create an app in the AINetwork Blockchain database](#create-an-app-in-the-ainetwork-blockchain-database)
  - [Set a value at a given path in the AINetwork Blockchain database](#set-a-value-at-a-given-path-in-the-ainetwork-blockchain-database)
  - [Set permissions for a path in the AINetwork Blockchain database](#set-permissions-for-a-path-in-the-ainetwork-blockchain-database)
  - [Retrieve the permissions for a path in the AINetwork Blockchain database](#retrieve-the-permissions-for-a-path-in-the-ainetwork-blockchain-database)
  - [Get AIN from faucet](#get-ain-from-faucet)
  - [Get AIN Balance](#get-ain-balance)
  - [Transfer AIN](#transfer-ain)

- [Get AIN Blockchain private key](#get-ain-blockchain-private-key)

- [Define App name to test](#define-app-name-to-test)

- [Create an app in the AINetwork Blockchain database](#create-an-app-in-the-ainetwork-blockchain-database)

- [Set a value at a given path in the AINetwork Blockchain database](#set-a-value-at-a-given-path-in-the-ainetwork-blockchain-database)

- [Set permissions for a path in the AINetwork Blockchain database](#set-permissions-for-a-path-in-the-ainetwork-blockchain-database)

- [Retrieve the permissions for a path in the AINetwork Blockchain database](#retrieve-the-permissions-for-a-path-in-the-ainetwork-blockchain-database)

- [Get AIN from faucet](#get-ain-from-faucet)

- [Get AIN Balance](#get-ain-balance)

- [Transfer AIN](#transfer-ain)
