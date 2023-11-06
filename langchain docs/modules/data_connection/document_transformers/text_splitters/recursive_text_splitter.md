# Recursively split by character

This text splitter is the recommended one for generic text. It is parameterized by a list of characters. It tries to split on them in order until the chunks are small enough. The default list is `["\n\n", "\n", " ", ""]`. This has the effect of trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be the strongest semantically related pieces of text.

1. How the text is split: by list of characters.
1. How the chunk size is measured: by number of characters.

```python
# This is a long document we can split up.  
with open('../../../state\_of\_the\_union.txt') as f:  
 state\_of\_the\_union = f.read()  

```

```python
from langchain.text\_splitter import RecursiveCharacterTextSplitter  

```

```python
text\_splitter = RecursiveCharacterTextSplitter(  
 # Set a really small chunk size, just to show.  
 chunk\_size = 100,  
 chunk\_overlap = 20,  
 length\_function = len,  
 is\_separator\_regex = False,  
)  

```

```python
texts = text\_splitter.create\_documents([state\_of\_the\_union])  
print(texts[0])  
print(texts[1])  

```

```text
 page\_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and' lookup\_str='' metadata={} lookup\_index=0  
 page\_content='of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.' lookup\_str='' metadata={} lookup\_index=0  

```

```python
text\_splitter.split\_text(state\_of\_the\_union)[:2]  

```

```text
 ['Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and',  
 'of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.']  

```
