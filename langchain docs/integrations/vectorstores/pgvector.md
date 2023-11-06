# PGVector

[PGVector](https://github.com/pgvector/pgvector) is an open-source vector similarity search for `Postgres`

It supports:

- exact and approximate nearest neighbor search
- L2 distance, inner product, and cosine distance

This notebook shows how to use the Postgres vector database (`PGVector`).

See the [installation instruction](https://github.com/pgvector/pgvector).

```bash
# Pip install necessary package  
pip install pgvector  
pip install openai  
pip install psycopg2-binary  
pip install tiktoken  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
## Loading Environment Variables  
from typing import List, Tuple  
from dotenv import load\_dotenv  
  
load\_dotenv()  

```

```text
 False  

```

```python
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.vectorstores.pgvector import PGVector  
from langchain.document\_loaders import TextLoader  
from langchain.docstore.document import Document  

```

```python
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  
  
embeddings = OpenAIEmbeddings()  

```

```python
# PGVector needs the connection string to the database.  
CONNECTION\_STRING = "postgresql+psycopg2://harrisonchase@localhost:5432/test3"  
  
# # Alternatively, you can create it from environment variables.  
# import os  
  
# CONNECTION\_STRING = PGVector.connection\_string\_from\_db\_params(  
# driver=os.environ.get("PGVECTOR\_DRIVER", "psycopg2"),  
# host=os.environ.get("PGVECTOR\_HOST", "localhost"),  
# port=int(os.environ.get("PGVECTOR\_PORT", "5432")),  
# database=os.environ.get("PGVECTOR\_DATABASE", "postgres"),  
# user=os.environ.get("PGVECTOR\_USER", "postgres"),  
# password=os.environ.get("PGVECTOR\_PASSWORD", "postgres"),  
# )  

```

## Similarity Search with Euclidean Distance (Default)[​](#similarity-search-with-euclidean-distance-default "Direct link to Similarity Search with Euclidean Distance (Default)")

```python
# The PGVector Module will try to create a table with the name of the collection.  
# So, make sure that the collection name is unique and the user has the permission to create a table.  
  
COLLECTION\_NAME = "state\_of\_the\_union\_test"  
  
db = PGVector.from\_documents(  
 embedding=embeddings,  
 documents=docs,  
 collection\_name=COLLECTION\_NAME,  
 connection\_string=CONNECTION\_STRING,  
)  

```

```python
query = "What did the president say about Ketanji Brown Jackson"  
docs\_with\_score = db.similarity\_search\_with\_score(query)  

```

```python
for doc, score in docs\_with\_score:  
 print("-" \* 80)  
 print("Score: ", score)  
 print(doc.page\_content)  
 print("-" \* 80)  

```

```text
 --------------------------------------------------------------------------------  
 Score: 0.18456886638850434  
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.21742627672631343  
 A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.   
   
 And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.   
   
 We can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling.   
   
 We’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers.   
   
 We’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.   
   
 We’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.22641793174529334  
 And for our LGBTQ+ Americans, let’s finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong.   
   
 As I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential.   
   
 While it often appears that we never agree, that isn’t true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice.   
   
 And soon, we’ll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things.   
   
 So tonight I’m offering a Unity Agenda for the Nation. Four big things we can do together.   
   
 First, beat the opioid epidemic.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.22670040608054465  
 Tonight, I’m announcing a crackdown on these companies overcharging American businesses and consumers.   
   
 And as Wall Street firms take over more nursing homes, quality in those homes has gone down and costs have gone up.   
   
 That ends on my watch.   
   
 Medicare is going to set higher standards for nursing homes and make sure your loved ones get the care they deserve and expect.   
   
 We’ll also cut costs and keep the economy going strong by giving workers a fair shot, provide more training and apprenticeships, hire them based on their skills not degrees.   
   
 Let’s pass the Paycheck Fairness Act and paid leave.   
   
 Raise the minimum wage to $15 an hour and extend the Child Tax Credit, so no one has to raise a family in poverty.   
   
 Let’s increase Pell Grants and increase our historic support of HBCUs, and invest in what Jill—our First Lady who teaches full-time—calls America’s best-kept secret: community colleges.  
 --------------------------------------------------------------------------------  

```

## Maximal Marginal Relevance Search (MMR)[​](#maximal-marginal-relevance-search-mmr "Direct link to Maximal Marginal Relevance Search (MMR)")

Maximal marginal relevance optimizes for similarity to query AND diversity among selected documents.

```python
docs\_with\_score = db.max\_marginal\_relevance\_search\_with\_score(query)  

```

```python
for doc, score in docs\_with\_score:  
 print("-" \* 80)  
 print("Score: ", score)  
 print(doc.page\_content)  
 print("-" \* 80)  

```

```text
 --------------------------------------------------------------------------------  
 Score: 0.18453882564037527  
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.23523731441720075  
 We can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together.   
   
 I recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera.   
   
 They were responding to a 9-1-1 call when a man shot and killed them with a stolen gun.   
   
 Officer Mora was 27 years old.   
   
 Officer Rivera was 22.   
   
 Both Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers.   
   
 I spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.   
   
 I’ve worked on these issues a long time.   
   
 I know what works: Investing in crime prevention and community police officers who’ll walk the beat, who’ll know the neighborhood, and who can restore trust and safety.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.2448441215698569  
 One was stationed at bases and breathing in toxic smoke from “burn pits” that incinerated wastes of war—medical and hazard material, jet fuel, and more.   
   
 When they came home, many of the world’s fittest and best trained warriors were never the same.   
   
 Headaches. Numbness. Dizziness.   
   
 A cancer that would put them in a flag-draped coffin.   
   
 I know.   
   
 One of those soldiers was my son Major Beau Biden.   
   
 We don’t know for sure if a burn pit was the cause of his brain cancer, or the diseases of so many of our troops.   
   
 But I’m committed to finding out everything we can.   
   
 Committed to military families like Danielle Robinson from Ohio.   
   
 The widow of Sergeant First Class Heath Robinson.   
   
 He was born a soldier. Army National Guard. Combat medic in Kosovo and Iraq.   
   
 Stationed near Baghdad, just yards from burn pits the size of football fields.   
   
 Heath’s widow Danielle is here with us tonight. They loved going to Ohio State football games. He loved building Legos with their daughter.  
 --------------------------------------------------------------------------------  
 --------------------------------------------------------------------------------  
 Score: 0.2513994424701056  
 And I’m taking robust action to make sure the pain of our sanctions is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers.   
   
 Tonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.   
   
 America will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.   
   
 These steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming.   
   
 But I want you to know that we are going to be okay.   
   
 When the history of this era is written Putin’s war on Ukraine will have left Russia weaker and the rest of the world stronger.   
   
 While it shouldn’t have taken something so terrible for people around the world to see what’s at stake now everyone sees it clearly.  
 --------------------------------------------------------------------------------  

```

## Working with vectorstore[​](#working-with-vectorstore "Direct link to Working with vectorstore")

Above, we created a vectorstore from scratch. However, often times we want to work with an existing vectorstore.
In order to do that, we can initialize it directly.

```python
store = PGVector(  
 collection\_name=COLLECTION\_NAME,  
 connection\_string=CONNECTION\_STRING,  
 embedding\_function=embeddings,  
)  

```

### Add documents[​](#add-documents "Direct link to Add documents")

We can add documents to the existing vectorstore.

```python
store.add\_documents([Document(page\_content="foo")])  

```

```text
 ['048c2e14-1cf3-11ee-8777-e65801318980']  

```

```python
docs\_with\_score = db.similarity\_search\_with\_score("foo")  

```

```python
docs\_with\_score[0]  

```

```text
 (Document(page\_content='foo', metadata={}), 3.3203430005457335e-09)  

```

```python
docs\_with\_score[1]  

```

```text
 (Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 0.2404395365581814)  

```

### Overriding a vectorstore[​](#overriding-a-vectorstore "Direct link to Overriding a vectorstore")

If you have an existing collection, you override it by doing `from_documents` and setting `pre_delete_collection` = True

```python
db = PGVector.from\_documents(  
 documents=docs,  
 embedding=embeddings,  
 collection\_name=COLLECTION\_NAME,  
 connection\_string=CONNECTION\_STRING,  
 pre\_delete\_collection=True,  
)  

```

```python
docs\_with\_score = db.similarity\_search\_with\_score("foo")  

```

```python
docs\_with\_score[0]  

```

```text
 (Document(page\_content='A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she’s been nominated, she’s received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans. \n\nAnd if we are to advance liberty and justice, we need to secure the Border and fix the immigration system. \n\nWe can do both. At our border, we’ve installed new technology like cutting-edge scanners to better detect drug smuggling. \n\nWe’ve set up joint patrols with Mexico and Guatemala to catch more human traffickers. \n\nWe’re putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster. \n\nWe’re securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 0.2404115088144465)  

```

### Using a VectorStore as a Retriever[​](#using-a-vectorstore-as-a-retriever "Direct link to Using a VectorStore as a Retriever")

```python
retriever = store.as\_retriever()  

```

```python
print(retriever)  

```

```text
 tags=None metadata=None vectorstore=<langchain.vectorstores.pgvector.PGVector object at 0x29f94f880> search\_type='similarity' search\_kwargs={}  

```

- [Similarity Search with Euclidean Distance (Default)](#similarity-search-with-euclidean-distance-default)

- [Maximal Marginal Relevance Search (MMR)](#maximal-marginal-relevance-search-mmr)

- [Working with vectorstore](#working-with-vectorstore)

  - [Add documents](#add-documents)
  - [Overriding a vectorstore](#overriding-a-vectorstore)
  - [Using a VectorStore as a Retriever](#using-a-vectorstore-as-a-retriever)

- [Add documents](#add-documents)

- [Overriding a vectorstore](#overriding-a-vectorstore)

- [Using a VectorStore as a Retriever](#using-a-vectorstore-as-a-retriever)
