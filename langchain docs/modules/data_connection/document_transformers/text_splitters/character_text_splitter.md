# Split by character

This is the simplest method. This splits based on characters (by default "\\n\\n") and measure chunk length by number of characters.

1. How the text is split: by single character.
1. How the chunk size is measured: by number of characters.

```python
# This is a long document we can split up.  
with open('../../../state\_of\_the\_union.txt') as f:  
 state\_of\_the\_union = f.read()  

```

```python
from langchain.text\_splitter import CharacterTextSplitter  
text\_splitter = CharacterTextSplitter(  
 separator = "\n\n",  
 chunk\_size = 1000,  
 chunk\_overlap = 200,  
 length\_function = len,  
 is\_separator\_regex = False,  
)  

```

```python
texts = text\_splitter.create\_documents([state\_of\_the\_union])  
print(texts[0])  

```

```text
 page\_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans. \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.' lookup\_str='' metadata={} lookup\_index=0  

```

Here's an example of passing metadata along with the documents, notice that it is split along with the documents.

```python
metadatas = [{"document": 1}, {"document": 2}]  
documents = text\_splitter.create\_documents([state\_of\_the\_union, state\_of\_the\_union], metadatas=metadatas)  
print(documents[0])  

```

```text
 page\_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans. \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.' lookup\_str='' metadata={'document': 1} lookup\_index=0  

```

```python
text\_splitter.split\_text(state\_of\_the\_union)[0]  

```

```text
 'Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans. \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.'  

```
