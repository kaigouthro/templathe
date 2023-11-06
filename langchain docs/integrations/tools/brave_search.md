# Brave Search

This notebook goes over how to use the Brave Search tool.

```python
from langchain.tools import BraveSearch  

```

```python
api\_key = "API KEY"  

```

```python
tool = BraveSearch.from\_api\_key(api\_key=api\_key, search\_kwargs={"count": 3})  

```

```python
tool.run("obama middle name")  

```

```text
 '[{"title": "Obama\'s Middle Name -- My Last Name -- is \'Hussein.\' So?", "link": "https://www.cair.com/cair\_in\_the\_news/obamas-middle-name-my-last-name-is-hussein-so/", "snippet": "I wasn\\u2019t sure whether to laugh or cry a few days back listening to radio talk show host Bill Cunningham repeatedly scream Barack <strong>Obama</strong>\\u2019<strong>s</strong> <strong>middle</strong> <strong>name</strong> \\u2014 my last <strong>name</strong> \\u2014 as if he had anti-Muslim Tourette\\u2019s. \\u201cHussein,\\u201d Cunningham hissed like he was beckoning Satan when shouting the ..."}, {"title": "What\'s up with Obama\'s middle name? - Quora", "link": "https://www.quora.com/Whats-up-with-Obamas-middle-name", "snippet": "Answer (1 of 15): A better question would be, \\u201cWhat\\u2019s up with <strong>Obama</strong>\\u2019s first <strong>name</strong>?\\u201d President Barack Hussein <strong>Obama</strong>\\u2019s father\\u2019s <strong>name</strong> was Barack Hussein <strong>Obama</strong>. He was <strong>named</strong> after his father. Hussein, <strong>Obama</strong>\\u2019<strong>s</strong> <strong>middle</strong> <strong>name</strong>, is a very common Arabic <strong>name</strong>, meaning &quot;good,&quot; &quot;handsome,&quot; or ..."}, {"title": "Barack Obama | Biography, Parents, Education, Presidency, Books, ...", "link": "https://www.britannica.com/biography/Barack-Obama", "snippet": "Barack <strong>Obama</strong>, in full Barack Hussein <strong>Obama</strong> II, (born August 4, 1961, Honolulu, Hawaii, U.S.), 44th president of the United States (2009\\u201317) and the first African American to hold the office. Before winning the presidency, <strong>Obama</strong> represented Illinois in the U.S."}]'  

```
