# Clarifai

[Clarifai](https://www.clarifai.com/) is an AI Platform that provides the full AI lifecycle ranging from data exploration, data labeling, model training, evaluation, and inference. A Clarifai application can be used as a vector database after uploading inputs.

This notebook shows how to use functionality related to the `Clarifai` vector database. Examples are shown to demonstrate text semantic search capabilities. Clarifai also supports semantic search with images, video frames, and localized search (see [Rank](https://docs.clarifai.com/api-guide/search/rank)) and attribute search (see [Filter](https://docs.clarifai.com/api-guide/search/filter)).

To use Clarifai, you must have an account and a Personal Access Token (PAT) key.
[Check here](https://clarifai.com/settings/security) to get or create a PAT.

# Dependencies

```bash
# Install required dependencies  
pip install clarifai  

```

# Imports

Here we will be setting the personal access token. You can find your PAT under settings/security on the platform.

```python
# Please login and get your API key from https://clarifai.com/settings/security  
from getpass import getpass  
  
CLARIFAI\_PAT = getpass()  

```

```text
 ········  

```

```python
# Import the required modules  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
from langchain.vectorstores import Clarifai  

```

# Setup

Setup the user id and app id where the text data will be uploaded. Note: when creating that application please select an appropriate base workflow for indexing your text documents such as the Language-Understanding workflow.

You will have to first create an account on [Clarifai](https://clarifai.com/login) and then create an application.

```python
USER\_ID = "USERNAME\_ID"  
APP\_ID = "APPLICATION\_ID"  
NUMBER\_OF\_DOCS = 4  

```

## From Texts[​](#from-texts "Direct link to From Texts")

Create a Clarifai vectorstore from a list of texts. This section will upload each text with its respective metadata to a Clarifai Application. The Clarifai Application can then be used for semantic search to find relevant texts.

```python
texts = [  
 "I really enjoy spending time with you",  
 "I hate spending time with my dog",  
 "I want to go for a run",  
 "I went to the movies yesterday",  
 "I love playing soccer with my friends",  
]  
  
metadatas = [{"id": i, "text": text, "source": "book 1", "category": ["books", "modern"]} for i, text in enumerate(texts)]  

```

```python
clarifai\_vector\_db = Clarifai.from\_texts(  
 user\_id=USER\_ID,  
 app\_id=APP\_ID,  
 texts=texts,  
 pat=CLARIFAI\_PAT,  
 number\_of\_docs=NUMBER\_OF\_DOCS,  
 metadatas=metadatas,  
)  

```

```python
docs = clarifai\_vector\_db.similarity\_search("I would love to see you")  
docs  

```

```text
 [Document(page\_content='I really enjoy spending time with you', metadata={'text': 'I really enjoy spending time with you', 'id': 0.0, 'source': 'book 1', 'category': ['books', 'modern']}),  
 Document(page\_content='I went to the movies yesterday', metadata={'text': 'I went to the movies yesterday', 'id': 3.0, 'source': 'book 1', 'category': ['books', 'modern']})]  

```

```python
# There is lots powerful filtering you can do within an app by leveraging metadata filters.   
# This one will limit the similarity query to only the texts that have key of "source" matching value of "book 1"  
book1\_similar\_docs = clarifai\_vector\_db.similarity\_search("I would love to see you", filter={"source": "book 1"})  
  
# you can also use lists in the input's metadata and then select things that match an item in the list. This is useful for categories like below:  
book\_category\_similar\_docs = clarifai\_vector\_db.similarity\_search("I would love to see you", filter={"category": ["books"]})  

```

## From Documents[​](#from-documents "Direct link to From Documents")

Create a Clarifai vectorstore from a list of Documents. This section will upload each document with its respective metadata to a Clarifai Application. The Clarifai Application can then be used for semantic search to find relevant documents.

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

```python
docs[:4]  

```

```text
 [Document(page\_content='Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans. \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='Groups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland. \n\nIn this struggle as President Zelenskyy said in his speech to the European Parliament “Light will win over darkness.” The Ukrainian Ambassador to the United States is here tonight. \n\nLet each of us here tonight in this Chamber send an unmistakable signal to Ukraine and to the world. \n\nPlease rise if you are able and show that, Yes, we the United States of America stand with the Ukrainian people. \n\nThroughout our history we’ve learned this lesson when dictators do not pay a price for their aggression they cause more chaos. \n\nThey keep moving. \n\nAnd the costs and the threats to America and the world keep rising. \n\nThat’s why the NATO Alliance was created to secure peace and stability in Europe after World War 2. \n\nThe United States is a member along with 29 other nations. \n\nIt matters. American diplomacy matters. American resolve matters.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='Putin’s latest attack on Ukraine was premeditated and unprovoked. \n\nHe rejected repeated efforts at diplomacy. \n\nHe thought the West and NATO wouldn’t respond. And he thought he could divide us at home. Putin was wrong. We were ready. Here is what we did. \n\nWe prepared extensively and carefully. \n\nWe spent months building a coalition of other freedom-loving nations from Europe and the Americas to Asia and Africa to confront Putin. \n\nI spent countless hours unifying our European allies. We shared with the world in advance what we knew Putin was planning and precisely how he would try to falsely justify his aggression. \n\nWe countered Russia’s lies with truth. \n\nAnd now that he has acted the free world is holding him accountable. \n\nAlong with twenty-seven members of the European Union including France, Germany, Italy, as well as countries like the United Kingdom, Canada, Japan, Korea, Australia, New Zealand, and many others, even Switzerland.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='We are inflicting pain on Russia and supporting the people of Ukraine. Putin is now isolated from the world more than ever. \n\nTogether with our allies –we are right now enforcing powerful economic sanctions. \n\nWe are cutting off Russia’s largest banks from the international financial system. \n\nPreventing Russia’s central bank from defending the Russian Ruble making Putin’s $630 Billion “war fund” worthless. \n\nWe are choking off Russia’s access to technology that will sap its economic strength and weaken its military for years to come. \n\nTonight I say to the Russian oligarchs and corrupt leaders who have bilked billions of dollars off this violent regime no more. \n\nThe U.S. Department of Justice is assembling a dedicated task force to go after the crimes of Russian oligarchs. \n\nWe are joining with our European allies to find and seize your yachts your luxury apartments your private jets. We are coming for your ill-begotten gains.', metadata={'source': '../../../state\_of\_the\_union.txt'})]  

```

```python
USER\_ID = "USERNAME\_ID"  
APP\_ID = "APPLICATION\_ID"  
NUMBER\_OF\_DOCS = 4  

```

```python
clarifai\_vector\_db = Clarifai.from\_documents(  
 user\_id=USER\_ID,  
 app\_id=APP\_ID,  
 documents=docs,  
 pat=CLARIFAI\_PAT,  
 number\_of\_docs=NUMBER\_OF\_DOCS,  
)  

```

```python
docs = clarifai\_vector\_db.similarity\_search("Texts related to criminals and violence")  
docs  

```

```text
 [Document(page\_content='And I will keep doing everything in my power to crack down on gun trafficking and ghost guns you can buy online and make at home—they have no serial numbers and can’t be traced. \n\nAnd I ask Congress to pass proven measures to reduce gun violence. Pass universal background checks. Why should anyone on a terrorist list be able to purchase a weapon? \n\nBan assault weapons and high-capacity magazines. \n\nRepeal the liability shield that makes gun manufacturers the only industry in America that can’t be sued. \n\nThese laws don’t infringe on the Second Amendment. They save lives. \n\nThe most fundamental right in America is the right to vote – and to have it counted. And it’s under assault. \n\nIn state after state, new laws have been passed, not only to suppress the vote, but to subvert entire elections. \n\nWe cannot let this happen.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='We can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves. \n\nI’ve worked on these issues a long time. \n\nI know what works: Investing in crime prevention and community police officers who’ll walk the beat, who’ll know the neighborhood, and who can restore trust and safety.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 Document(page\_content='So let’s not abandon our streets. Or choose between safety and equal justice. \n\nLet’s come together to protect our communities, restore trust, and hold law enforcement accountable. \n\nThat’s why the Justice Department required body cameras, banned chokeholds, and restricted no-knock warrants for its officers. \n\nThat’s why the American Rescue Plan provided $350 Billion that cities, states, and counties can use to hire more police and invest in proven strategies like community violence interruption—trusted messengers breaking the cycle of violence and trauma and giving young people hope. \n\nWe should all agree: The answer is not to Defund the police. The answer is to FUND the police with the resources and training they need to protect our communities. \n\nI ask Democrats and Republicans alike: Pass my budget and keep our neighborhoods safe.', metadata={'source': '../../../state\_of\_the\_union.txt'})]  

```

## From existing App[​](#from-existing-app "Direct link to From existing App")

Within Clarifai we have great tools for adding data to applications (essentially projects) via API or UI. Most users will already have done that before interacting with LangChain so this example will use the data in an existing app to perform searches. Check out our [API docs](https://docs.clarifai.com/api-guide/data/create-get-update-delete) and [UI docs](https://docs.clarifai.com/portal-guide/data). The Clarifai Application can then be used for semantic search to find relevant documents.

```python
USER\_ID = "USERNAME\_ID"  
APP\_ID = "APPLICATION\_ID"  
NUMBER\_OF\_DOCS = 4  

```

```python
clarifai\_vector\_db = Clarifai(  
 user\_id=USER\_ID,  
 app\_id=APP\_ID,  
 pat=CLARIFAI\_PAT,  
 number\_of\_docs=NUMBER\_OF\_DOCS,  
)  

```

```python
docs = clarifai\_vector\_db.similarity\_search("Texts related to criminals and violence")  
docs  

```

- [From Texts](#from-texts)
- [From Documents](#from-documents)
- [From existing App](#from-existing-app)
