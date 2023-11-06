# Split code

CodeTextSplitter allows you to split your code with multiple languages supported. Import enum `Language` and specify the language.

```python
from langchain.text\_splitter import (  
 RecursiveCharacterTextSplitter,  
 Language,  
)  

```

```python
# Full list of support languages  
[e.value for e in Language]  

```

```text
 ['cpp',  
 'go',  
 'java',  
 'kotlin',  
 'js',  
 'ts',  
 'php',  
 'proto',  
 'python',  
 'rst',  
 'ruby',  
 'rust',  
 'scala',  
 'swift',  
 'markdown',  
 'latex',  
 'html',  
 'sol',  
 'csharp']  

```

```python
# You can also see the separators used for a given language  
RecursiveCharacterTextSplitter.get\_separators\_for\_language(Language.PYTHON)  

```

```text
 ['\nclass ', '\ndef ', '\n\tdef ', '\n\n', '\n', ' ', '']  

```

## Python[​](#python "Direct link to Python")

Here's an example using the PythonTextSplitter:

```python
PYTHON\_CODE = """  
def hello\_world():  
 print("Hello, World!")  
  
# Call the function  
hello\_world()  
"""  
python\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.PYTHON, chunk\_size=50, chunk\_overlap=0  
)  
python\_docs = python\_splitter.create\_documents([PYTHON\_CODE])  
python\_docs  

```

```text
 [Document(page\_content='def hello\_world():\n print("Hello, World!")', metadata={}),  
 Document(page\_content='# Call the function\nhello\_world()', metadata={})]  

```

## JS[​](#js "Direct link to JS")

Here's an example using the JS text splitter:

```python
JS\_CODE = """  
function helloWorld() {  
 console.log("Hello, World!");  
}  
  
// Call the function  
helloWorld();  
"""  
  
js\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.JS, chunk\_size=60, chunk\_overlap=0  
)  
js\_docs = js\_splitter.create\_documents([JS\_CODE])  
js\_docs  

```

```text
 [Document(page\_content='function helloWorld() {\n console.log("Hello, World!");\n}', metadata={}),  
 Document(page\_content='// Call the function\nhelloWorld();', metadata={})]  

```

## TS[​](#ts "Direct link to TS")

Here's an example using the TS text splitter:

```python
TS\_CODE = """  
function helloWorld(): void {  
 console.log("Hello, World!");  
}  
  
// Call the function  
helloWorld();  
"""  
  
ts\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.TS, chunk\_size=60, chunk\_overlap=0  
)  
ts\_docs = ts\_splitter.create\_documents([TS\_CODE])  
ts\_docs  

```

```text
 [Document(page\_content='function helloWorld(): void {\n console.log("Hello, World!");\n}', metadata={}),  
 Document(page\_content='// Call the function\nhelloWorld();', metadata={})]  

```

## Markdown[​](#markdown "Direct link to Markdown")

Here's an example using the Markdown text splitter:

````python
markdown\_text = """  
# 🦜️🔗 LangChain  
  
⚡ Building applications with LLMs through composability ⚡  
  
## Quick Install  
  
```bash  
# Hopefully this code block isn't split  
pip install langchain  
````

As an open-source project in a rapidly developing field, we are extremely open to contributions.\
"""

````



```python
md\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.MARKDOWN, chunk\_size=60, chunk\_overlap=0  
)  
md\_docs = md\_splitter.create\_documents([markdown\_text])  
md\_docs  

````

````text
 [Document(page\_content='# 🦜️🔗 LangChain', metadata={}),  
 Document(page\_content='⚡ Building applications with LLMs through composability ⚡', metadata={}),  
 Document(page\_content='## Quick Install', metadata={}),  
 Document(page\_content="```bash\n# Hopefully this code block isn't split", metadata={}),  
 Document(page\_content='pip install langchain', metadata={}),  
 Document(page\_content='```', metadata={}),  
 Document(page\_content='As an open-source project in a rapidly developing field, we', metadata={}),  
 Document(page\_content='are extremely open to contributions.', metadata={})]  

````

## Latex[​](#latex "Direct link to Latex")

Here's an example on Latex text:

```python
latex\_text = """  
\documentclass{article}  
  
\begin{document}  
  
\maketitle  
  
\section{Introduction}  
Large language models (LLMs) are a type of machine learning model that can be trained on vast amounts of text data to generate human-like language. In recent years, LLMs have made significant advances in a variety of natural language processing tasks, including language translation, text generation, and sentiment analysis.  
  
\subsection{History of LLMs}  
The earliest LLMs were developed in the 1980s and 1990s, but they were limited by the amount of data that could be processed and the computational power available at the time. In the past decade, however, advances in hardware and software have made it possible to train LLMs on massive datasets, leading to significant improvements in performance.  
  
\subsection{Applications of LLMs}  
LLMs have many applications in industry, including chatbots, content creation, and virtual assistants. They can also be used in academia for research in linguistics, psychology, and computational linguistics.  
  
\end{document}  
"""  

```

```python
latex\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.MARKDOWN, chunk\_size=60, chunk\_overlap=0  
)  
latex\_docs = latex\_splitter.create\_documents([latex\_text])  
latex\_docs  

```

```text
 [Document(page\_content='\\documentclass{article}\n\n\x08egin{document}\n\n\\maketitle', metadata={}),  
 Document(page\_content='\\section{Introduction}', metadata={}),  
 Document(page\_content='Large language models (LLMs) are a type of machine learning', metadata={}),  
 Document(page\_content='model that can be trained on vast amounts of text data to', metadata={}),  
 Document(page\_content='generate human-like language. In recent years, LLMs have', metadata={}),  
 Document(page\_content='made significant advances in a variety of natural language', metadata={}),  
 Document(page\_content='processing tasks, including language translation, text', metadata={}),  
 Document(page\_content='generation, and sentiment analysis.', metadata={}),  
 Document(page\_content='\\subsection{History of LLMs}', metadata={}),  
 Document(page\_content='The earliest LLMs were developed in the 1980s and 1990s,', metadata={}),  
 Document(page\_content='but they were limited by the amount of data that could be', metadata={}),  
 Document(page\_content='processed and the computational power available at the', metadata={}),  
 Document(page\_content='time. In the past decade, however, advances in hardware and', metadata={}),  
 Document(page\_content='software have made it possible to train LLMs on massive', metadata={}),  
 Document(page\_content='datasets, leading to significant improvements in', metadata={}),  
 Document(page\_content='performance.', metadata={}),  
 Document(page\_content='\\subsection{Applications of LLMs}', metadata={}),  
 Document(page\_content='LLMs have many applications in industry, including', metadata={}),  
 Document(page\_content='chatbots, content creation, and virtual assistants. They', metadata={}),  
 Document(page\_content='can also be used in academia for research in linguistics,', metadata={}),  
 Document(page\_content='psychology, and computational linguistics.', metadata={}),  
 Document(page\_content='\\end{document}', metadata={})]  

```

## HTML[​](#html "Direct link to HTML")

Here's an example using an HTML text splitter:

```python
html\_text = """  
<!DOCTYPE html>  
<html>  
 <head>  
 <title>🦜️🔗 LangChain</title>  
 <style>  
 body {  
 font-family: Arial, sans-serif;  
 }  
 h1 {  
 color: darkblue;  
 }  
 </style>  
 </head>  
 <body>  
 <div>  
 <h1>🦜️🔗 LangChain</h1>  
 <p>⚡ Building applications with LLMs through composability ⚡</p>  
 </div>  
 <div>  
 As an open-source project in a rapidly developing field, we are extremely open to contributions.  
 </div>  
 </body>  
</html>  
"""  

```

```python
html\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.HTML, chunk\_size=60, chunk\_overlap=0  
)  
html\_docs = html\_splitter.create\_documents([html\_text])  
html\_docs  

```

```text
 [Document(page\_content='<!DOCTYPE html>\n<html>', metadata={}),  
 Document(page\_content='<head>\n <title>🦜️🔗 LangChain</title>', metadata={}),  
 Document(page\_content='<style>\n body {\n font-family: Aria', metadata={}),  
 Document(page\_content='l, sans-serif;\n }\n h1 {', metadata={}),  
 Document(page\_content='color: darkblue;\n }\n </style>\n </head', metadata={}),  
 Document(page\_content='>', metadata={}),  
 Document(page\_content='<body>', metadata={}),  
 Document(page\_content='<div>\n <h1>🦜️🔗 LangChain</h1>', metadata={}),  
 Document(page\_content='<p>⚡ Building applications with LLMs through composability ⚡', metadata={}),  
 Document(page\_content='</p>\n </div>', metadata={}),  
 Document(page\_content='<div>\n As an open-source project in a rapidly dev', metadata={}),  
 Document(page\_content='eloping field, we are extremely open to contributions.', metadata={}),  
 Document(page\_content='</div>\n </body>\n</html>', metadata={})]  

```

## Solidity[​](#solidity "Direct link to Solidity")

Here's an example using the Solidity text splitter:

```python
SOL\_CODE = """  
pragma solidity ^0.8.20;  
contract HelloWorld {  
 function add(uint a, uint b) pure public returns(uint) {  
 return a + b;  
 }  
}  
"""  
  
sol\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.SOL, chunk\_size=128, chunk\_overlap=0  
)  
sol\_docs = sol\_splitter.create\_documents([SOL\_CODE])  
sol\_docs  

```

```text
[  
 Document(page\_content='pragma solidity ^0.8.20;', metadata={}),  
 Document(page\_content='contract HelloWorld {\n function add(uint a, uint b) pure public returns(uint) {\n return a + b;\n }\n}', metadata={})  
]  

```

## C#[​](#c "Direct link to C#")

Here's an example using the C# text splitter:

```csharp
using System;  
class Program  
{  
 static void Main()  
 {  
 int age = 30; // Change the age value as needed  
  
 // Categorize the age without any console output  
 if (age < 18)  
 {  
 // Age is under 18  
 }  
 else if (age >= 18 && age < 65)  
 {  
 // Age is an adult  
 }  
 else  
 {  
 // Age is a senior citizen  
 }  
 }  
}  

```

```text
 [Document(page\_content='using System;', metadata={}),  
 Document(page\_content='class Program\n{', metadata={}),  
 Document(page\_content='static void', metadata={}),  
 Document(page\_content='Main()', metadata={}),  
 Document(page\_content='{', metadata={}),  
 Document(page\_content='int age', metadata={}),  
 Document(page\_content='= 30; // Change', metadata={}),  
 Document(page\_content='the age value', metadata={}),  
 Document(page\_content='as needed', metadata={}),  
 Document(page\_content='//', metadata={}),  
 Document(page\_content='Categorize the', metadata={}),  
 Document(page\_content='age without any', metadata={}),  
 Document(page\_content='console output', metadata={}),  
 Document(page\_content='if (age', metadata={}),  
 Document(page\_content='< 18)', metadata={}),  
 Document(page\_content='{', metadata={}),  
 Document(page\_content='//', metadata={}),  
 Document(page\_content='Age is under 18', metadata={}),  
 Document(page\_content='}', metadata={}),  
 Document(page\_content='else if', metadata={}),  
 Document(page\_content='(age >= 18 &&', metadata={}),  
 Document(page\_content='age < 65)', metadata={}),  
 Document(page\_content='{', metadata={}),  
 Document(page\_content='//', metadata={}),  
 Document(page\_content='Age is an adult', metadata={}),  
 Document(page\_content='}', metadata={}),  
 Document(page\_content='else', metadata={}),  
 Document(page\_content='{', metadata={}),  
 Document(page\_content='//', metadata={}),  
 Document(page\_content='Age is a senior', metadata={}),  
 Document(page\_content='citizen', metadata={}),  
 Document(page\_content='}\n }', metadata={}),  
 Document(page\_content='}', metadata={})]  

```

- [Python](#python)
- [JS](#js)
- [TS](#ts)
- [Markdown](#markdown)
- [Latex](#latex)
- [HTML](#html)
- [Solidity](#solidity)
- [C#](#c)
