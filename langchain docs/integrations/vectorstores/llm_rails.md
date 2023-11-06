# LLMRails

[LLMRails](https://www.llmrails.com/) is a API platform for building GenAI applications. It provides an easy-to-use API for document indexing and querying that is managed by LLMRails and is optimized for performance and accuracy.
See the [LLMRails API documentation](https://docs.llmrails.com/)  for more information on how to use the API.

This notebook shows how to use functionality related to the `LLMRails`'s integration with langchain.
Note that unlike many other integrations in this category, LLMRails provides an end-to-end managed service for retrieval augmented generation, which includes:

1. A way to extract text from document files and chunk them into sentences.
1. Its own embeddings model and vector store - each text segment is encoded into a vector embedding and stored in the LLMRails internal vector store
1. A query service that automatically encodes the query into embedding, and retrieves the most relevant text segments (including support for [Hybrid Search](https://docs.llmrails.com/datastores/search))

All of these are supported in this LangChain integration.

# Setup

You will need a LLMRails account to use LLMRails with LangChain. To get started, use the following steps:

1. [Sign up](https://console.llmrails.com/signup) for a LLMRails account if you don't already have one.
1. Next you'll need to create API keys to access the API. Click on the **"API Keys"** tab in the corpus view and then the **"Create API Key"** button. Give your key a name. Click "Create key" and you now have an active API key. Keep this key confidential.

To use LangChain with LLMRails, you'll need to have this value: api_key.
You can provide those to LangChain in two ways:

1. Include in your environment these two variables: `LLM_RAILS_API_KEY`, `LLM_RAILS_DATASTORE_ID`.

For example, you can set these variables using os.environ and getpass as follows:

```python
import os  
import getpass  
  
os.environ["LLM\_RAILS\_API\_KEY"] = getpass.getpass("LLMRails API Key:")  
os.environ["LLM\_RAILS\_DATASTORE\_ID"] = getpass.getpass("LLMRails Datastore Id:")  

```

1. Provide them as arguments when creating the LLMRails vectorstore object:

```python
vectorstore = LLMRails(  
 api\_key=llm\_rails\_api\_key,  
 datastore\_id=datastore\_id  
)  

```

## Adding text[​](#adding-text "Direct link to Adding text")

For adding text to your datastore first you have to go to [Datastores](https://console.llmrails.com/datastores) page and create one. Click Create Datastore button and choose a name and embedding model for your datastore. Then get your datastore id from newly created datatore settings.

```python
from langchain.vectorstores import LLMRails  
import os  
  
os.environ['LLM\_RAILS\_DATASTORE\_ID'] = 'Your datastore id '  
os.environ['LLM\_RAILS\_API\_KEY'] = 'Your API Key'  
  
llm\_rails = LLMRails.from\_texts(['Your text here'])  

```

## Similarity search[​](#similarity-search "Direct link to Similarity search")

The simplest scenario for using LLMRails is to perform a similarity search.

```python
query = "What do you plan to do about national security?"  
found\_docs = llm\_rails.similarity\_search(  
 query, k=5  
)  

```

```python
print(found\_docs[0].page\_content)  

```

```text
 Others may not be democratic but nevertheless depend upon a rules-based international system.  
   
 Yet what we share in common, and the prospect of a freer and more open world, makes such a broad coalition necessary and worthwhile.  
   
 We will listen to and consider ideas that our partners suggest about how to do this.  
   
 Building this inclusive coalition requires reinforcing the multilateral system to uphold the founding principles of the United Nations, including respect for international law.  
   
 141 countries expressed support at the United Nations General Assembly for a resolution condemning Russia’s unprovoked aggression against Ukraine.  
   
 We continue to demonstrate this approach by engaging all regions across all issues, not in terms of what we are against but what we are for.  
   
 This year, we partnered with ASEAN to advance clean energy infrastructure and maritime security in the region.  
   
 We kickstarted the Prosper Africa Build Together Campaign to fuel economic growth across the continent and bolster trade and investment in the clean energy, health, and digital technology sectors.  
   
 We are working to develop a partnership with countries on the Atlantic Ocean to establish and carry out a shared approach to advancing our joint development, economic, environmental, scientific, and maritime governance goals.  
   
 We galvanized regional action to address the core challenges facing the Western Hemisphere by spearheading the Americas Partnership for Economic Prosperity to drive economic recovery and by mobilizing the region behind a bold and unprecedented approach to migration through the Los Angeles Declaration on Migration and Protection.  
   
 In the Middle East, we have worked to enhance deterrence toward Iran, de-escalate regional conflicts, deepen integration among a diverse set of partners in the region, and bolster energy stability.  
   
 A prime example of an inclusive coalition is IPEF, which we launched alongside a dozen regional partners that represent 40 percent of the world’s GDP.  

```

## Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

Sometimes we might want to perform the search, but also obtain a relevancy score to know how good is a particular result.

```python
query = "What is your approach to national defense"  
found\_docs = llm\_rails.similarity\_search\_with\_score(  
 query, k=5,  
)  

```

```python
document, score = found\_docs[0]  
print(document.page\_content)  
print(f"\nScore: {score}")  

```

```text
 But we will do so as the last resort and only when the objectives and mission are clear and achievable, consistent with our values and laws, alongside non-military tools, and the mission is undertaken with the informed consent of the American people.  
   
 Our approach to national defense is described in detail in the 2022 National Defense Strategy.  
   
 Our starting premise is that a powerful U.S. military helps advance and safeguard vital U.S. national interests by backstopping diplomacy, confronting aggression, deterring conflict, projecting strength, and protecting the American people and their economic interests.  
   
 Amid intensifying competition, the military’s role is to maintain and gain warfighting advantages while limiting those of our competitors.  
   
 The military will act urgently to sustain and strengthen deterrence, with the PRC as its pacing challenge.  
   
 We will make disciplined choices regarding our national defense and focus our attention on the military’s primary responsibilities: to defend the homeland, and deter attacks and aggression against the United States, our allies and partners, while being prepared to fight and win the Nation’s wars should diplomacy and deterrence fail.  
   
 To do so, we will combine our strengths to achieve maximum effect in deterring acts of aggression—an approach we refer to as integrated deterrence (see text box on page 22).  
   
 We will operate our military using a campaigning mindset—sequencing logically linked military activities to advance strategy-aligned priorities.  
   
 And, we will build a resilient force and defense ecosystem to ensure we can perform these functions for decades to come.  
   
 We ended America’s longest war in Afghanistan, and with it an era of major military operations to remake other societies, even as we have maintained the capacity to address terrorist threats to the American people as they emerge.  
   
 20 NATIONAL SECURITY STRATEGY Page 21   
   
 A combat-credible military is the foundation of deterrence and America’s ability to prevail in conflict.  
   
 Score: 0.5040982687179959  

```

## LLMRails as a Retriever[​](#llmrails-as-a-retriever "Direct link to LLMRails as a Retriever")

LLMRails, as all the other LangChain vectorstores, is most often used as a LangChain Retriever:

```python
retriever = llm\_rails.as\_retriever()  
retriever  

```

```text
 LLMRailsRetriever(tags=None, metadata=None, vectorstore=<langchain.vectorstores.llm\_rails.LLMRails object at 0x107b9c040>, search\_type='similarity', search\_kwargs={'k': 5})  

```

```python
query = "What is your approach to national defense"  
retriever.get\_relevant\_documents(query)[0]  

```

```text
 Document(page\_content='But we will do so as the last resort and only when the objectives and mission are clear and achievable, consistent with our values and laws, alongside non-military tools, and the mission is undertaken with the informed consent of the American people.\n\nOur approach to national defense is described in detail in the 2022 National Defense Strategy.\n\nOur starting premise is that a powerful U.S. military helps advance and safeguard vital U.S. national interests by backstopping diplomacy, confronting aggression, deterring conflict, projecting strength, and protecting the American people and their economic interests.\n\nAmid intensifying competition, the military’s role is to maintain and gain warfighting advantages while limiting those of our competitors.\n\nThe military will act urgently to sustain and strengthen deterrence, with the PRC as its pacing challenge.\n\nWe will make disciplined choices regarding our national defense and focus our attention on the military’s primary responsibilities: to defend the homeland, and deter attacks and aggression against the United States, our allies and partners, while being prepared to fight and win the Nation’s wars should diplomacy and deterrence fail.\n\nTo do so, we will combine our strengths to achieve maximum effect in deterring acts of aggression—an approach we refer to as integrated deterrence (see text box on page 22).\n\nWe will operate our military using a campaigning mindset—sequencing logically linked military activities to advance strategy-aligned priorities.\n\nAnd, we will build a resilient force and defense ecosystem to ensure we can perform these functions for decades to come.\n\nWe ended America’s longest war in Afghanistan, and with it an era of major military operations to remake other societies, even as we have maintained the capacity to address terrorist threats to the American people as they emerge.\n\n20 NATIONAL SECURITY STRATEGY Page 21 \x90\x90\x90\x90\x90\x90\n\nA combat-credible military is the foundation of deterrence and America’s ability to prevail in conflict.', metadata={'type': 'file', 'url': 'https://cdn.llmrails.com/dst\_d94b490c-4638-4247-ad5e-9aa0e7ef53c1/c2d63a2ea3cd406cb522f8312bc1535d', 'name': 'Biden-Harris-Administrations-National-Security-Strategy-10.2022.pdf'})  

```

- [Adding text](#adding-text)
- [Similarity search](#similarity-search)
- [Similarity search with score](#similarity-search-with-score)
- [LLMRails as a Retriever](#llmrails-as-a-retriever)
