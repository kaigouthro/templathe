# Serialization

It is often preferable to store prompts not as python code but as files. This can make it easy to share, store, and version prompts. This notebook covers how to do that in LangChain, walking through all the different types of prompts and the different serialization options.

At a high level, the following design principles are applied to serialization:

1. Both JSON and YAML are supported. We want to support serialization methods that are human readable on disk, and YAML and JSON are two of the most popular methods for that. Note that this rule applies to prompts. For other assets, like examples, different serialization methods may be supported.
1. We support specifying everything in one file, or storing different components (templates, examples, etc) in different files and referencing them. For some cases, storing everything in file makes the most sense, but for others it is preferable to split up some of the assets (long templates, large examples, reusable components). LangChain supports both.

Both JSON and YAML are supported. We want to support serialization methods that are human readable on disk, and YAML and JSON are two of the most popular methods for that. Note that this rule applies to prompts. For other assets, like examples, different serialization methods may be supported.

We support specifying everything in one file, or storing different components (templates, examples, etc) in different files and referencing them. For some cases, storing everything in file makes the most sense, but for others it is preferable to split up some of the assets (long templates, large examples, reusable components). LangChain supports both.

There is also a single entry point to load prompts from disk, making it easy to load any type of prompt.

```python
# All prompts are loaded through the `load\_prompt` function.  
from langchain.prompts import load\_prompt  

```

## PromptTemplate[​](#prompttemplate "Direct link to PromptTemplate")

This section covers examples for loading a PromptTemplate.

### Loading from YAML[​](#loading-from-yaml "Direct link to Loading from YAML")

This shows an example of loading a PromptTemplate from YAML.

```bash
cat simple\_prompt.yaml  

```

```text
 \_type: prompt  
 input\_variables:  
 ["adjective", "content"]  
 template:   
 Tell me a {adjective} joke about {content}.  

```

```python
prompt = load\_prompt("simple\_prompt.yaml")  
print(prompt.format(adjective="funny", content="chickens"))  

```

```text
 Tell me a funny joke about chickens.  

```

### Loading from JSON[​](#loading-from-json "Direct link to Loading from JSON")

This shows an example of loading a PromptTemplate from JSON.

```bash
cat simple\_prompt.json  

```

```text
 {  
 "\_type": "prompt",  
 "input\_variables": ["adjective", "content"],  
 "template": "Tell me a {adjective} joke about {content}."  
 }  

```

```python
prompt = load\_prompt("simple\_prompt.json")  
print(prompt.format(adjective="funny", content="chickens"))  

```

Tell me a funny joke about chickens.

### Loading template from a file[​](#loading-template-from-a-file "Direct link to Loading template from a file")

This shows an example of storing the template in a separate file and then referencing it in the config. Notice that the key changes from `template` to `template_path`.

```bash
cat simple\_template.txt  

```

```text
 Tell me a {adjective} joke about {content}.  

```

```bash
cat simple\_prompt\_with\_template\_file.json  

```

```text
 {  
 "\_type": "prompt",  
 "input\_variables": ["adjective", "content"],  
 "template\_path": "simple\_template.txt"  
 }  

```

```python
prompt = load\_prompt("simple\_prompt\_with\_template\_file.json")  
print(prompt.format(adjective="funny", content="chickens"))  

```

```text
 Tell me a funny joke about chickens.  

```

## FewShotPromptTemplate[​](#fewshotprompttemplate "Direct link to FewShotPromptTemplate")

This section covers examples for loading few-shot prompt templates.

### Examples[​](#examples "Direct link to Examples")

This shows an example of what examples stored as json might look like.

```bash
cat examples.json  

```

```text
 [  
 {"input": "happy", "output": "sad"},  
 {"input": "tall", "output": "short"}  
 ]  

```

And here is what the same examples stored as yaml might look like.

```bash
cat examples.yaml  

```

```text
 - input: happy  
 output: sad  
 - input: tall  
 output: short  

```

### Loading from YAML[​](#loading-from-yaml-1 "Direct link to Loading from YAML")

This shows an example of loading a few-shot example from YAML.

```bash
cat few\_shot\_prompt.yaml  

```

```text
 \_type: few\_shot  
 input\_variables:  
 ["adjective"]  
 prefix:   
 Write antonyms for the following words.  
 example\_prompt:  
 \_type: prompt  
 input\_variables:  
 ["input", "output"]  
 template:  
 "Input: {input}\nOutput: {output}"  
 examples:  
 examples.json  
 suffix:  
 "Input: {adjective}\nOutput:"  

```

```python
prompt = load\_prompt("few\_shot\_prompt.yaml")  
print(prompt.format(adjective="funny"))  

```

```text
 Write antonyms for the following words.  
   
 Input: happy  
 Output: sad  
   
 Input: tall  
 Output: short  
   
 Input: funny  
 Output:  

```

The same would work if you loaded examples from the yaml file.

```bash
cat few\_shot\_prompt\_yaml\_examples.yaml  

```

```text
 \_type: few\_shot  
 input\_variables:  
 ["adjective"]  
 prefix:   
 Write antonyms for the following words.  
 example\_prompt:  
 \_type: prompt  
 input\_variables:  
 ["input", "output"]  
 template:  
 "Input: {input}\nOutput: {output}"  
 examples:  
 examples.yaml  
 suffix:  
 "Input: {adjective}\nOutput:"  

```

```python
prompt = load\_prompt("few\_shot\_prompt\_yaml\_examples.yaml")  
print(prompt.format(adjective="funny"))  

```

```text
 Write antonyms for the following words.  
   
 Input: happy  
 Output: sad  
   
 Input: tall  
 Output: short  
   
 Input: funny  
 Output:  

```

### Loading from JSON[​](#loading-from-json-1 "Direct link to Loading from JSON")

This shows an example of loading a few-shot example from JSON.

```bash
cat few\_shot\_prompt.json  

```

```text
 {  
 "\_type": "few\_shot",  
 "input\_variables": ["adjective"],  
 "prefix": "Write antonyms for the following words.",  
 "example\_prompt": {  
 "\_type": "prompt",  
 "input\_variables": ["input", "output"],  
 "template": "Input: {input}\nOutput: {output}"  
 },  
 "examples": "examples.json",  
 "suffix": "Input: {adjective}\nOutput:"  
 }   

```

```python
prompt = load\_prompt("few\_shot\_prompt.json")  
print(prompt.format(adjective="funny"))  

```

```text
 Write antonyms for the following words.  
   
 Input: happy  
 Output: sad  
   
 Input: tall  
 Output: short  
   
 Input: funny  
 Output:  

```

### Examples in the config[​](#examples-in-the-config "Direct link to Examples in the config")

This shows an example of referencing the examples directly in the config.

```bash
cat few\_shot\_prompt\_examples\_in.json  

```

```text
 {  
 "\_type": "few\_shot",  
 "input\_variables": ["adjective"],  
 "prefix": "Write antonyms for the following words.",  
 "example\_prompt": {  
 "\_type": "prompt",  
 "input\_variables": ["input", "output"],  
 "template": "Input: {input}\nOutput: {output}"  
 },  
 "examples": [  
 {"input": "happy", "output": "sad"},  
 {"input": "tall", "output": "short"}  
 ],  
 "suffix": "Input: {adjective}\nOutput:"  
 }   

```

```python
prompt = load\_prompt("few\_shot\_prompt\_examples\_in.json")  
print(prompt.format(adjective="funny"))  

```

```text
 Write antonyms for the following words.  
   
 Input: happy  
 Output: sad  
   
 Input: tall  
 Output: short  
   
 Input: funny  
 Output:  

```

### Example prompt from a file[​](#example-prompt-from-a-file "Direct link to Example prompt from a file")

This shows an example of loading the PromptTemplate that is used to format the examples from a separate file. Note that the key changes from `example_prompt` to `example_prompt_path`.

```bash
cat example\_prompt.json  

```

```text
 {  
 "\_type": "prompt",  
 "input\_variables": ["input", "output"],  
 "template": "Input: {input}\nOutput: {output}"   
 }  

```

```bash
cat few\_shot\_prompt\_example\_prompt.json  

```

```text
 {  
 "\_type": "few\_shot",  
 "input\_variables": ["adjective"],  
 "prefix": "Write antonyms for the following words.",  
 "example\_prompt\_path": "example\_prompt.json",  
 "examples": "examples.json",  
 "suffix": "Input: {adjective}\nOutput:"  
 }   

```

```python
prompt = load\_prompt("few\_shot\_prompt\_example\_prompt.json")  
print(prompt.format(adjective="funny"))  

```

```text
 Write antonyms for the following words.  
   
 Input: happy  
 Output: sad  
   
 Input: tall  
 Output: short  
   
 Input: funny  
 Output:  

```

## PromptTemplate with OutputParser[​](#prompttemplate-with-outputparser "Direct link to PromptTemplate with OutputParser")

This shows an example of loading a prompt along with an OutputParser from a file.

```bash
cat prompt\_with\_output\_parser.json  

```

```text
 {  
 "input\_variables": [  
 "question",  
 "student\_answer"  
 ],  
 "output\_parser": {  
 "regex": "(.\*?)\\nScore: (.\*)",  
 "output\_keys": [  
 "answer",  
 "score"  
 ],  
 "default\_output\_key": null,  
 "\_type": "regex\_parser"  
 },  
 "partial\_variables": {},  
 "template": "Given the following question and student answer, provide a correct answer and score the student answer.\nQuestion: {question}\nStudent Answer: {student\_answer}\nCorrect Answer:",  
 "template\_format": "f-string",  
 "validate\_template": true,  
 "\_type": "prompt"  
 }  

```

```python
prompt = load\_prompt("prompt\_with\_output\_parser.json")  

```

```python
prompt.output\_parser.parse(  
 "George Washington was born in 1732 and died in 1799.\nScore: 1/2"  
)  

```

```text
 {'answer': 'George Washington was born in 1732 and died in 1799.',  
 'score': '1/2'}  

```

- [PromptTemplate](#prompttemplate)

  - [Loading from YAML](#loading-from-yaml)
  - [Loading from JSON](#loading-from-json)
  - [Loading template from a file](#loading-template-from-a-file)

- [FewShotPromptTemplate](#fewshotprompttemplate)

  - [Examples](#examples)
  - [Loading from YAML](#loading-from-yaml-1)
  - [Loading from JSON](#loading-from-json-1)
  - [Examples in the config](#examples-in-the-config)
  - [Example prompt from a file](#example-prompt-from-a-file)

- [PromptTemplate with OutputParser](#prompttemplate-with-outputparser)

- [Loading from YAML](#loading-from-yaml)

- [Loading from JSON](#loading-from-json)

- [Loading template from a file](#loading-template-from-a-file)

- [Examples](#examples)

- [Loading from YAML](#loading-from-yaml-1)

- [Loading from JSON](#loading-from-json-1)

- [Examples in the config](#examples-in-the-config)

- [Example prompt from a file](#example-prompt-from-a-file)
