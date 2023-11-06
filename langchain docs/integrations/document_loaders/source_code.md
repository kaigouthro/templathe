# Source Code

This notebook covers how to load source code files using a special approach with language parsing: each top-level function and class in the code is loaded into separate documents. Any remaining code top-level code outside the already loaded functions and classes will be loaded into a separate document.

This approach can potentially improve the accuracy of QA models over source code. Currently, the supported languages for code parsing are Python and JavaScript. The language used for parsing can be configured, along with the minimum number of lines required to activate the splitting based on syntax.

```bash
pip install esprima  

```

```python
import warnings  
  
warnings.filterwarnings("ignore")  
from pprint import pprint  
from langchain.text\_splitter import Language  
from langchain.document\_loaders.generic import GenericLoader  
from langchain.document\_loaders.parsers import LanguageParser  

```

```python
loader = GenericLoader.from\_filesystem(  
 "./example\_data/source\_code",  
 glob="\*",  
 suffixes=[".py", ".js"],  
 parser=LanguageParser(),  
)  
docs = loader.load()  

```

```python
len(docs)  

```

```text
 6  

```

```python
for document in docs:  
 pprint(document.metadata)  

```

```text
 {'content\_type': 'functions\_classes',  
 'language': <Language.PYTHON: 'python'>,  
 'source': 'example\_data/source\_code/example.py'}  
 {'content\_type': 'functions\_classes',  
 'language': <Language.PYTHON: 'python'>,  
 'source': 'example\_data/source\_code/example.py'}  
 {'content\_type': 'simplified\_code',  
 'language': <Language.PYTHON: 'python'>,  
 'source': 'example\_data/source\_code/example.py'}  
 {'content\_type': 'functions\_classes',  
 'language': <Language.JS: 'js'>,  
 'source': 'example\_data/source\_code/example.js'}  
 {'content\_type': 'functions\_classes',  
 'language': <Language.JS: 'js'>,  
 'source': 'example\_data/source\_code/example.js'}  
 {'content\_type': 'simplified\_code',  
 'language': <Language.JS: 'js'>,  
 'source': 'example\_data/source\_code/example.js'}  

```

```python
print("\n\n--8<--\n\n".join([document.page\_content for document in docs]))  

```

```text
 class MyClass:  
 def \_\_init\_\_(self, name):  
 self.name = name  
   
 def greet(self):  
 print(f"Hello, {self.name}!")  
   
 --8<--  
   
 def main():  
 name = input("Enter your name: ")  
 obj = MyClass(name)  
 obj.greet()  
   
 --8<--  
   
 # Code for: class MyClass:  
   
   
 # Code for: def main():  
   
   
 if \_\_name\_\_ == "\_\_main\_\_":  
 main()  
   
 --8<--  
   
 class MyClass {  
 constructor(name) {  
 this.name = name;  
 }  
   
 greet() {  
 console.log(`Hello, ${this.name}!`);  
 }  
 }  
   
 --8<--  
   
 function main() {  
 const name = prompt("Enter your name:");  
 const obj = new MyClass(name);  
 obj.greet();  
 }  
   
 --8<--  
   
 // Code for: class MyClass {  
   
 // Code for: function main() {  
   
 main();  

```

The parser can be disabled for small files.

The parameter `parser_threshold` indicates the minimum number of lines that the source code file must have to be segmented using the parser.

```python
loader = GenericLoader.from\_filesystem(  
 "./example\_data/source\_code",  
 glob="\*",  
 suffixes=[".py"],  
 parser=LanguageParser(language=Language.PYTHON, parser\_threshold=1000),  
)  
docs = loader.load()  

```

```python
len(docs)  

```

```text
 1  

```

```python
print(docs[0].page\_content)  

```

```text
 class MyClass:  
 def \_\_init\_\_(self, name):  
 self.name = name  
   
 def greet(self):  
 print(f"Hello, {self.name}!")  
   
   
 def main():  
 name = input("Enter your name: ")  
 obj = MyClass(name)  
 obj.greet()  
   
   
 if \_\_name\_\_ == "\_\_main\_\_":  
 main()  
   

```

## Splitting[​](#splitting "Direct link to Splitting")

Additional splitting could be needed for those functions, classes, or scripts that are too big.

```python
loader = GenericLoader.from\_filesystem(  
 "./example\_data/source\_code",  
 glob="\*",  
 suffixes=[".js"],  
 parser=LanguageParser(language=Language.JS),  
)  
docs = loader.load()  

```

```python
from langchain.text\_splitter import (  
 RecursiveCharacterTextSplitter,  
 Language,  
)  

```

```python
js\_splitter = RecursiveCharacterTextSplitter.from\_language(  
 language=Language.JS, chunk\_size=60, chunk\_overlap=0  
)  

```

```python
result = js\_splitter.split\_documents(docs)  

```

```python
len(result)  

```

```text
 7  

```

```python
print("\n\n--8<--\n\n".join([document.page\_content for document in result]))  

```

```text
 class MyClass {  
 constructor(name) {  
 this.name = name;  
   
 --8<--  
   
 }  
   
 --8<--  
   
 greet() {  
 console.log(`Hello, ${this.name}!`);  
 }  
 }  
   
 --8<--  
   
 function main() {  
 const name = prompt("Enter your name:");  
   
 --8<--  
   
 const obj = new MyClass(name);  
 obj.greet();  
 }  
   
 --8<--  
   
 // Code for: class MyClass {  
   
 // Code for: function main() {  
   
 --8<--  
   
 main();  

```

- [Splitting](#splitting)
