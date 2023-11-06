# HTML to text

[html2text](https://github.com/Alir3z4/html2text/) is a Python package that converts a page of `HTML` into clean, easy-to-read plain `ASCII text`.

The ASCII also happens to be a valid `Markdown` (a text-to-HTML format).

```bash
pip install html2text  

```

```python
from langchain.document\_loaders import AsyncHtmlLoader  
  
urls = ["https://www.espn.com", "https://lilianweng.github.io/posts/2023-06-23-agent/"]  
loader = AsyncHtmlLoader(urls)  
docs = loader.load()  

```

```text
 Fetching pages: 100%|############| 2/2 [00:00<00:00, 10.75it/s]  

```

```python
from langchain.document\_transformers import Html2TextTransformer  

```

```python
urls = ["https://www.espn.com", "https://lilianweng.github.io/posts/2023-06-23-agent/"]  
html2text = Html2TextTransformer()  
docs\_transformed = html2text.transform\_documents(docs)  

```

```python
docs\_transformed[0].page\_content[1000:2000]  

```

```text
 " \* ESPNFC\n\n \* X Games\n\n \* SEC Network\n\n## ESPN Apps\n\n \* ESPN\n\n \* ESPN Fantasy\n\n## Follow ESPN\n\n \* Facebook\n\n \* Twitter\n\n \* Instagram\n\n \* Snapchat\n\n \* YouTube\n\n \* The ESPN Daily Podcast\n\n2023 FIFA Women's World Cup\n\n## Follow live: Canada takes on Nigeria in group stage of Women's World Cup\n\n2m\n\nEPA/Morgan Hancock\n\n## TOP HEADLINES\n\n \* Snyder fined $60M over findings in investigation\n \* NFL owners approve $6.05B sale of Commanders\n \* Jags assistant comes out as gay in NFL milestone\n \* O's alone atop East after topping slumping Rays\n \* ACC's Phillips: Never condoned hazing at NU\n\n \* Vikings WR Addison cited for driving 140 mph\n \* 'Taking his time': Patient QB Rodgers wows Jets\n \* Reyna got U.S. assurances after Berhalter rehire\n \* NFL Future Power Rankings\n\n## USWNT AT THE WORLD CUP\n\n### USA VS. VIETNAM: 9 P.M. ET FRIDAY\n\n## How do you defend against Alex Morgan? Former opponents sound off\n\nThe U.S. forward is unstoppable at this level, scoring 121 goals and adding 49"  

```

```python
docs\_transformed[1].page\_content[1000:2000]  

```

```text
 "t's brain,\ncomplemented by several key components:\n\n \* \*\*Planning\*\*\n \* Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks.\n \* Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results.\n \* \*\*Memory\*\*\n \* Short-term memory: I would consider all the in-context learning (See Prompt Engineering) as utilizing short-term memory of the model to learn.\n \* Long-term memory: This provides the agent with the capability to retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval.\n \* \*\*Tool use\*\*\n \* The agent learns to call external APIs for extra information that is missing from the model weights (often hard to change after pre-training), including current information, code execution c"  

```
