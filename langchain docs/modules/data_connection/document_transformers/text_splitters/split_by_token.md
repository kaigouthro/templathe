# Split by tokens

Language models have a token limit. You should not exceed the token limit. When you split your text into chunks it is therefore a good idea to count the number of tokens. There are many tokenizers. When you count tokens in your text you should use the same tokenizer as used in the language model.

## tiktoken[​](#tiktoken "Direct link to tiktoken")

[tiktoken](https://github.com/openai/tiktoken) is a fast `BPE` tokenizer created by `OpenAI`.

We can use it to estimate tokens used. It will probably be more accurate for the OpenAI models.

1. How the text is split: by character passed in.
1. How the chunk size is measured: by `tiktoken` tokenizer.

```python
#!pip install tiktoken  

```

```python
# This is a long document we can split up.  
with open("../../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
from langchain.text\_splitter import CharacterTextSplitter  

```

```python
text\_splitter = CharacterTextSplitter.from\_tiktoken\_encoder(  
 chunk\_size=100, chunk\_overlap=0  
)  
texts = text\_splitter.split\_text(state\_of\_the\_union)  

```

```python
print(texts[0])  

```

```text
 Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.   
   
 Last year COVID-19 kept us apart. This year we are finally together again.   
   
 Tonight, we meet as Democrats Republicans and Independents. But most importantly as Americans.   
   
 With a duty to one another to the American people to the Constitution.  

```

Note that if we use `CharacterTextSplitter.from_tiktoken_encoder`, text is only split by `CharacterTextSplitter` and `tiktoken` tokenizer is used to merge splits. It means that split can be larger than chunk size measured by `tiktoken` tokenizer. We can use `RecursiveCharacterTextSplitter.from_tiktoken_encoder` to make sure splits are not larger than chunk size of tokens allowed by the language model, where each split will be recursively split if it has a larger size.

We can also load a tiktoken splitter directly, which ensure each split is smaller than chunk size.

```python
from langchain.text\_splitter import TokenTextSplitter  
  
text\_splitter = TokenTextSplitter(chunk\_size=10, chunk\_overlap=0)  
  
texts = text\_splitter.split\_text(state\_of\_the\_union)  
print(texts[0])  

```

## spaCy[​](#spacy "Direct link to spaCy")

[spaCy](https://spacy.io/) is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython.

Another alternative to `NLTK` is to use [spaCy tokenizer](https://spacy.io/api/tokenizer).

1. How the text is split: by `spaCy` tokenizer.
1. How the chunk size is measured: by number of characters.

```python
#!pip install spacy  

```

```python
# This is a long document we can split up.  
with open("../../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  

```

```python
from langchain.text\_splitter import SpacyTextSplitter  
  
text\_splitter = SpacyTextSplitter(chunk\_size=1000)  

```

```python
texts = text\_splitter.split\_text(state\_of\_the\_union)  
print(texts[0])  

```

```text
 Madam Speaker, Madam Vice President, our First Lady and Second Gentleman.  
   
 Members of Congress and the Cabinet.  
   
 Justices of the Supreme Court.  
   
 My fellow Americans.   
   
   
   
 Last year COVID-19 kept us apart.  
   
 This year we are finally together again.   
   
   
   
 Tonight, we meet as Democrats Republicans and Independents.  
   
 But most importantly as Americans.   
   
   
   
 With a duty to one another to the American people to the Constitution.   
   
   
   
 And with an unwavering resolve that freedom will always triumph over tyranny.   
   
   
   
 Six days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways.  
   
 But he badly miscalculated.   
   
   
   
 He thought he could roll into Ukraine and the world would roll over.  
   
 Instead he met a wall of strength he never imagined.   
   
   
   
 He met the Ukrainian people.   
   
   
   
 From President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.  

```

## SentenceTransformers[​](#sentencetransformers "Direct link to SentenceTransformers")

The `SentenceTransformersTokenTextSplitter` is a specialized text splitter for use with the sentence-transformer models. The default behaviour is to split the text into chunks that fit the token window of the sentence transformer model that you would like to use.

```python
from langchain.text\_splitter import SentenceTransformersTokenTextSplitter  

```

```python
splitter = SentenceTransformersTokenTextSplitter(chunk\_overlap=0)  
text = "Lorem "  

```

```python
count\_start\_and\_stop\_tokens = 2  
text\_token\_count = splitter.count\_tokens(text=text) - count\_start\_and\_stop\_tokens  
print(text\_token\_count)  

```

```text
 2  

```

```python
token\_multiplier = splitter.maximum\_tokens\_per\_chunk // text\_token\_count + 1  
  
# `text\_to\_split` does not fit in a single chunk  
text\_to\_split = text \* token\_multiplier  
  
print(f"tokens in text to split: {splitter.count\_tokens(text=text\_to\_split)}")  

```

```text
 tokens in text to split: 514  

```

```python
text\_chunks = splitter.split\_text(text=text\_to\_split)  
  
print(text\_chunks[1])  

```

```text
 lorem  

```

## NLTK[​](#nltk "Direct link to NLTK")

[The Natural Language Toolkit](https://en.wikipedia.org/wiki/Natural_Language_Toolkit), or more commonly [NLTK](https://www.nltk.org/), is a suite of libraries and programs for symbolic and statistical natural language processing (NLP) for English written in the Python programming language.

Rather than just splitting on "\\n\\n", we can use `NLTK` to split based on [NLTK tokenizers](https://www.nltk.org/api/nltk.tokenize.html).

1. How the text is split: by `NLTK` tokenizer.
1. How the chunk size is measured: by number of characters.

```python
# pip install nltk  

```

```python
# This is a long document we can split up.  
with open("../../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  

```

```python
from langchain.text\_splitter import NLTKTextSplitter  
  
text\_splitter = NLTKTextSplitter(chunk\_size=1000)  

```

```python
texts = text\_splitter.split\_text(state\_of\_the\_union)  
print(texts[0])  

```

```text
 Madam Speaker, Madam Vice President, our First Lady and Second Gentleman.  
   
 Members of Congress and the Cabinet.  
   
 Justices of the Supreme Court.  
   
 My fellow Americans.  
   
 Last year COVID-19 kept us apart.  
   
 This year we are finally together again.  
   
 Tonight, we meet as Democrats Republicans and Independents.  
   
 But most importantly as Americans.  
   
 With a duty to one another to the American people to the Constitution.  
   
 And with an unwavering resolve that freedom will always triumph over tyranny.  
   
 Six days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways.  
   
 But he badly miscalculated.  
   
 He thought he could roll into Ukraine and the world would roll over.  
   
 Instead he met a wall of strength he never imagined.  
   
 He met the Ukrainian people.  
   
 From President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.  
   
 Groups of citizens blocking tanks with their bodies.  

```

## Hugging Face tokenizer[​](#hugging-face-tokenizer "Direct link to Hugging Face tokenizer")

[Hugging Face](https://huggingface.co/docs/tokenizers/index) has many tokenizers.

We use Hugging Face tokenizer, the [GPT2TokenizerFast](https://huggingface.co/Ransaka/gpt2-tokenizer-fast) to count the text length in tokens.

1. How the text is split: by character passed in.
1. How the chunk size is measured: by number of tokens calculated by the `Hugging Face` tokenizer.

```python
from transformers import GPT2TokenizerFast  
  
tokenizer = GPT2TokenizerFast.from\_pretrained("gpt2")  

```

```python
# This is a long document we can split up.  
with open("../../../state\_of\_the\_union.txt") as f:  
 state\_of\_the\_union = f.read()  
from langchain.text\_splitter import CharacterTextSplitter  

```

```python
text\_splitter = CharacterTextSplitter.from\_huggingface\_tokenizer(  
 tokenizer, chunk\_size=100, chunk\_overlap=0  
)  
texts = text\_splitter.split\_text(state\_of\_the\_union)  

```

```python
print(texts[0])  

```

```text
 Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.   
   
 Last year COVID-19 kept us apart. This year we are finally together again.   
   
 Tonight, we meet as Democrats Republicans and Independents. But most importantly as Americans.   
   
 With a duty to one another to the American people to the Constitution.  

```

- [tiktoken](#tiktoken)
- [spaCy](#spacy)
- [SentenceTransformers](#sentencetransformers)
- [NLTK](#nltk)
- [Hugging Face tokenizer](#hugging-face-tokenizer)
