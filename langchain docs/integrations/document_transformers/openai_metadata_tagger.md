# OpenAI metadata tagger

It can often be useful to tag ingested documents with structured metadata, such as the title, tone, or length of a document, to allow for a more targeted similarity search later. However, for large numbers of documents, performing this labelling process manually can be tedious.

The `OpenAIMetadataTagger` document transformer automates this process by extracting metadata from each provided document according to a provided schema. It uses a configurable `OpenAI Functions`-powered chain under the hood, so if you pass a custom LLM instance, it must be an `OpenAI` model with functions support.

**Note:** This document transformer works best with complete documents, so it's best to run it first with whole documents before doing any other splitting or processing!

For example, let's say you wanted to index a set of movie reviews. You could initialize the document transformer with a valid `JSON Schema` object as follows:

```python
from langchain.schema import Document  
from langchain.chat\_models import ChatOpenAI  
from langchain.document\_transformers.openai\_functions import create\_metadata\_tagger  

```

```python
schema = {  
 "properties": {  
 "movie\_title": {"type": "string"},  
 "critic": {"type": "string"},  
 "tone": {"type": "string", "enum": ["positive", "negative"]},  
 "rating": {  
 "type": "integer",  
 "description": "The number of stars the critic rated the movie",  
 },  
 },  
 "required": ["movie\_title", "critic", "tone"],  
}  
  
# Must be an OpenAI model that supports functions  
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")  
  
document\_transformer = create\_metadata\_tagger(metadata\_schema=schema, llm=llm)  

```

You can then simply pass the document transformer a list of documents, and it will extract metadata from the contents:

```python
original\_documents = [  
 Document(  
 page\_content="Review of The Bee Movie\nBy Roger Ebert\n\nThis is the greatest movie ever made. 4 out of 5 stars."  
 ),  
 Document(  
 page\_content="Review of The Godfather\nBy Anonymous\n\nThis movie was super boring. 1 out of 5 stars.",  
 metadata={"reliable": False},  
 ),  
]  
  
enhanced\_documents = document\_transformer.transform\_documents(original\_documents)  

```

```python
import json  
  
print(  
 \*[d.page\_content + "\n\n" + json.dumps(d.metadata) for d in enhanced\_documents],  
 sep="\n\n---------------\n\n"  
)  

```

```text
 Review of The Bee Movie  
 By Roger Ebert  
   
 This is the greatest movie ever made. 4 out of 5 stars.  
   
 {"movie\_title": "The Bee Movie", "critic": "Roger Ebert", "tone": "positive", "rating": 4}  
   
 ---------------  
   
 Review of The Godfather  
 By Anonymous  
   
 This movie was super boring. 1 out of 5 stars.  
   
 {"movie\_title": "The Godfather", "critic": "Anonymous", "tone": "negative", "rating": 1, "reliable": false}  

```

The new documents can then be further processed by a text splitter before being loaded into a vector store. Extracted fields will not overwrite existing metadata.

You can also initialize the document transformer with a Pydantic schema:

```python
from typing import Literal  
  
from pydantic import BaseModel, Field  
  
  
class Properties(BaseModel):  
 movie\_title: str  
 critic: str  
 tone: Literal["positive", "negative"]  
 rating: int = Field(description="Rating out of 5 stars")  
  
  
document\_transformer = create\_metadata\_tagger(Properties, llm)  
enhanced\_documents = document\_transformer.transform\_documents(original\_documents)  
  
print(  
 \*[d.page\_content + "\n\n" + json.dumps(d.metadata) for d in enhanced\_documents],  
 sep="\n\n---------------\n\n"  
)  

```

```text
 Review of The Bee Movie  
 By Roger Ebert  
   
 This is the greatest movie ever made. 4 out of 5 stars.  
   
 {"movie\_title": "The Bee Movie", "critic": "Roger Ebert", "tone": "positive", "rating": 4}  
   
 ---------------  
   
 Review of The Godfather  
 By Anonymous  
   
 This movie was super boring. 1 out of 5 stars.  
   
 {"movie\_title": "The Godfather", "critic": "Anonymous", "tone": "negative", "rating": 1, "reliable": false}  

```

## Customization[​](#customization "Direct link to Customization")

You can pass the underlying tagging chain the standard LLMChain arguments in the document transformer constructor. For example, if you wanted to ask the LLM to focus specific details in the input documents, or extract metadata in a certain style, you could pass in a custom prompt:

```python
from langchain.prompts import ChatPromptTemplate  
  
prompt = ChatPromptTemplate.from\_template(  
 """Extract relevant information from the following text.  
Anonymous critics are actually Roger Ebert.  
  
{input}  
"""  
)  
  
document\_transformer = create\_metadata\_tagger(schema, llm, prompt=prompt)  
enhanced\_documents = document\_transformer.transform\_documents(original\_documents)  
  
print(  
 \*[d.page\_content + "\n\n" + json.dumps(d.metadata) for d in enhanced\_documents],  
 sep="\n\n---------------\n\n"  
)  

```

```text
 Review of The Bee Movie  
 By Roger Ebert  
   
 This is the greatest movie ever made. 4 out of 5 stars.  
   
 {"movie\_title": "The Bee Movie", "critic": "Roger Ebert", "tone": "positive", "rating": 4}  
   
 ---------------  
   
 Review of The Godfather  
 By Anonymous  
   
 This movie was super boring. 1 out of 5 stars.  
   
 {"movie\_title": "The Godfather", "critic": "Roger Ebert", "tone": "negative", "rating": 1, "reliable": false}  

```

- [Customization](#customization)
