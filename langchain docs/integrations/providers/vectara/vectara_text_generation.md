# Vectara Text Generation

This notebook is based on [text generation](https://github.com/langchain-ai/langchain/blob/master/docs/modules/chains/index_examples/vector_db_text_generation.ipynb) notebook and adapted to Vectara.

## Prepare Data[​](#prepare-data "Direct link to Prepare Data")

First, we prepare the data. For this example, we fetch a documentation site that consists of markdown files hosted on Github and split them into small enough Documents.

```python
import os  
from langchain.llms import OpenAI  
from langchain.docstore.document import Document  
import requests  
from langchain.vectorstores import Vectara  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.prompts import PromptTemplate  
import pathlib  
import subprocess  
import tempfile  

```

```python
def get\_github\_docs(repo\_owner, repo\_name):  
 with tempfile.TemporaryDirectory() as d:  
 subprocess.check\_call(  
 f"git clone --depth 1 https://github.com/{repo\_owner}/{repo\_name}.git .",  
 cwd=d,  
 shell=True,  
 )  
 git\_sha = (  
 subprocess.check\_output("git rev-parse HEAD", shell=True, cwd=d)  
 .decode("utf-8")  
 .strip()  
 )  
 repo\_path = pathlib.Path(d)  
 markdown\_files = list(repo\_path.glob("\*/\*.md")) + list(  
 repo\_path.glob("\*/\*.mdx")  
 )  
 for markdown\_file in markdown\_files:  
 with open(markdown\_file, "r") as f:  
 relative\_path = markdown\_file.relative\_to(repo\_path)  
 github\_url = f"https://github.com/{repo\_owner}/{repo\_name}/blob/{git\_sha}/{relative\_path}"  
 yield Document(page\_content=f.read(), metadata={"source": github\_url})  
  
  
sources = get\_github\_docs("yirenlu92", "deno-manual-forked")  
  
source\_chunks = []  
splitter = CharacterTextSplitter(separator=" ", chunk\_size=1024, chunk\_overlap=0)  
for source in sources:  
 for chunk in splitter.split\_text(source.page\_content):  
 source\_chunks.append(chunk)  

```

```text
 Cloning into '.'...  

```

## Set Up Vector DB[​](#set-up-vector-db "Direct link to Set Up Vector DB")

Now that we have the documentation content in chunks, let's put all this information in a vector index for easy retrieval.

```python
search\_index = Vectara.from\_texts(source\_chunks, embedding=None)  

```

## Set Up LLM Chain with Custom Prompt[​](#set-up-llm-chain-with-custom-prompt "Direct link to Set Up LLM Chain with Custom Prompt")

Next, let's set up a simple LLM chain but give it a custom prompt for blog post generation. Note that the custom prompt is parameterized and takes two inputs: `context`, which will be the documents fetched from the vector search, and `topic`, which is given by the user.

```python
from langchain.chains import LLMChain  
  
prompt\_template = """Use the context below to write a 400 word blog post about the topic below:  
 Context: {context}  
 Topic: {topic}  
 Blog post:"""  
  
PROMPT = PromptTemplate(template=prompt\_template, input\_variables=["context", "topic"])  
  
llm = OpenAI(openai\_api\_key=os.environ["OPENAI\_API\_KEY"], temperature=0)  
  
chain = LLMChain(llm=llm, prompt=PROMPT)  

```

## Generate Text[​](#generate-text "Direct link to Generate Text")

Finally, we write a function to apply our inputs to the chain. The function takes an input parameter `topic`. We find the documents in the vector index that correspond to that `topic`, and use them as additional context in our simple LLM chain.

```python
def generate\_blog\_post(topic):  
 docs = search\_index.similarity\_search(topic, k=4)  
 inputs = [{"context": doc.page\_content, "topic": topic} for doc in docs]  
 print(chain.apply(inputs))  

```

```python
generate\_blog\_post("environment variables")  

```

````text
 [{'text': '\n\nWhen it comes to running Deno CLI tasks, environment variables can be a powerful tool for customizing the behavior of your tasks. With the Deno Task Definition interface, you can easily configure environment variables to be set when executing your tasks.\n\nThe Deno Task Definition interface is configured in a `tasks.json` within your workspace. It includes a `env` field, which allows you to specify any environment variables that should be set when executing the task. For example, if you wanted to set the `NODE\_ENV` environment variable to `production` when running a Deno task, you could add the following to your `tasks.json`:\n\n```json\n{\n "version": "2.0.0",\n "tasks": [\n {\n "type": "deno",\n "command": "run",\n "args": [\n "mod.ts"\n ],\n "env": {\n "NODE\_ENV": "production"\n },\n "problemMatcher": [\n "$deno"\n ],\n "label": "deno: run"\n }\n ]\n}\n```\n\nThe Deno language server and this extension also'}, {'text': '\n\nEnvironment variables are a great way to store and access data in your applications. They are especially useful when you need to store sensitive information such as API keys, passwords, and other credentials.\n\nDeno.env is a library that provides getter and setter methods for environment variables. This makes it easy to store and retrieve data from environment variables. For example, you can use the setter method to set a variable like this:\n\n```ts\nDeno.env.set("FIREBASE\_API\_KEY", "examplekey123");\nDeno.env.set("FIREBASE\_AUTH\_DOMAIN", "firebasedomain.com");\n```\n\nAnd then you can use the getter method to retrieve the data like this:\n\n```ts\nconsole.log(Deno.env.get("FIREBASE\_API\_KEY")); // examplekey123\nconsole.log(Deno.env.get("FIREBASE\_AUTH\_DOMAIN")); // firebasedomain.com\n```\n\nYou can also store environment variables in a `.env` file and retrieve them using `dotenv` in the standard'}, {'text': '\n\nEnvironment variables are a powerful tool for developers, allowing them to store and access data without hard-coding it into their applications. Deno, the secure JavaScript and TypeScript runtime, offers built-in support for environment variables with the `Deno.env` API.\n\nUsing `Deno.env` is simple. It has getter and setter methods that allow you to easily set and retrieve environment variables. For example, you can set the `FIREBASE\_API\_KEY` and `FIREBASE\_AUTH\_DOMAIN` environment variables like this:\n\n```ts\nDeno.env.set("FIREBASE\_API\_KEY", "examplekey123");\nDeno.env.set("FIREBASE\_AUTH\_DOMAIN", "firebasedomain.com");\n```\n\nAnd then you can retrieve them like this:\n\n```ts\nconsole.log(Deno.env.get("FIREBASE\_API\_KEY")); // examplekey123\nconsole.log(Deno.env.get("FIREBASE\_AUTH\_DOMAIN")); // firebasedomain.com\n```'}, {'text': '\n\nEnvironment variables are an important part of any programming language, and Deno is no exception. Environment variables are used to store information about the environment in which a program is running, such as the operating system, user preferences, and other settings. In Deno, environment variables are used to set up proxies, control the output of colors, and more.\n\nThe `NO\_PROXY` environment variable is a de facto standard in Deno that indicates which hosts should bypass the proxy set in other environment variables. This is useful for developers who want to access certain resources without having to go through a proxy. For more information on this standard, you can check out the website no-color.org.\n\nThe `Deno.noColor` environment variable is another important environment variable in Deno. This variable is used to control the output of colors in the Deno terminal. By setting this variable to true, you can disable the output of colors in the terminal. This can be useful for developers who want to focus on the output of their code without being distracted by the colors.\n\nFinally, the `Deno.env` environment variable is used to access the environment variables set in the Deno runtime. This variable is useful for developers who want'}]  

````

- [Prepare Data](#prepare-data)
- [Set Up Vector DB](#set-up-vector-db)
- [Set Up LLM Chain with Custom Prompt](#set-up-llm-chain-with-custom-prompt)
- [Generate Text](#generate-text)
