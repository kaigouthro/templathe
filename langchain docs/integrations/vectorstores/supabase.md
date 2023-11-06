# Supabase (Postgres)

[Supabase](https://supabase.com/docs) is an open-source Firebase alternative. `Supabase` is built on top of `PostgreSQL`, which offers strong SQL querying capabilities and enables a simple interface with already-existing tools and frameworks.

[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) also known as `Postgres`, is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

This notebook shows how to use `Supabase` and `pgvector` as your VectorStore.

To run this notebook, please ensure:

- the `pgvector` extension is enabled
- you have installed the `supabase-py` package
- that you have created a `match_documents` function in your database
- that you have a `documents` table in your `public` schema similar to the one below.

The following function determines cosine similarity, but you can adjust to your needs.

```sql
-- Enable the pgvector extension to work with embedding vectors  
create extension if not exists vector;  
  
-- Create a table to store your documents  
create table  
 documents (  
 id uuid primary key,  
 content text, -- corresponds to Document.pageContent  
 metadata jsonb, -- corresponds to Document.metadata  
 embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed  
 );  
  
-- Create a function to search for documents  
create function match\_documents (  
 query\_embedding vector (1536),  
 filter jsonb default '{}'  
) returns table (  
 id uuid,  
 content text,  
 metadata jsonb,  
 similarity float  
) language plpgsql as $$  
#variable\_conflict use\_column  
begin  
 return query  
 select  
 id,  
 content,  
 metadata,  
 1 - (documents.embedding <=> query\_embedding) as similarity  
 from documents  
 where metadata @> filter  
 order by documents.embedding <=> query\_embedding;  
end;  
$$;  

```

```bash
# with pip  
pip install supabase  
  
# with conda  
# !conda install -c conda-forge supabase  

```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

```python
import os  
import getpass  
  
os.environ["OPENAI\_API\_KEY"] = getpass.getpass("OpenAI API Key:")  

```

```python
os.environ["SUPABASE\_URL"] = getpass.getpass("Supabase URL:")  

```

```python
os.environ["SUPABASE\_SERVICE\_KEY"] = getpass.getpass("Supabase Service Key:")  

```

```python
# If you're storing your Supabase and OpenAI API keys in a .env file, you can load them with dotenv  
from dotenv import load\_dotenv  
  
load\_dotenv()  

```

First we'll create a Supabase client and instantiate a OpenAI embeddings class.

```python
import os  
from supabase.client import Client, create\_client  
from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.vectorstores import SupabaseVectorStore  
  
supabase\_url = os.environ.get("SUPABASE\_URL")  
supabase\_key = os.environ.get("SUPABASE\_SERVICE\_KEY")  
supabase: Client = create\_client(supabase\_url, supabase\_key)  
  
embeddings = OpenAIEmbeddings()  

```

Next we'll load and parse some data for our vector store (skip if you already have documents with embeddings stored in your DB).

```python
from langchain.text\_splitter import CharacterTextSplitter  
from langchain.document\_loaders import TextLoader  
  
loader = TextLoader("../../modules/state\_of\_the\_union.txt")  
documents = loader.load()  
text\_splitter = CharacterTextSplitter(chunk\_size=1000, chunk\_overlap=0)  
docs = text\_splitter.split\_documents(documents)  

```

Insert the above documents into the database. Embeddings will automatically be generated for each document.

```python
vector\_store = SupabaseVectorStore.from\_documents(docs, embeddings, client=supabase, table\_name="documents", query\_name="match\_documents")  

```

Alternatively if you already have documents with embeddings in your database, simply instantiate a new `SupabaseVectorStore` directly:

```python
vector\_store = SupabaseVectorStore(embedding=embeddings, client=supabase, table\_name="documents", query\_name="match\_documents")  

```

Finally, test it out by performing a similarity search:

```python
query = "What did the president say about Ketanji Brown Jackson"  
matched\_docs = vector\_store.similarity\_search(query)  

```

```python
print(matched\_docs[0].page\_content)  

```

```text
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  

```

## Similarity search with score[​](#similarity-search-with-score "Direct link to Similarity search with score")

The returned distance score is cosine distance. Therefore, a lower score is better.

```python
matched\_docs = vector\_store.similarity\_search\_with\_relevance\_scores(query)  

```

```python
matched\_docs[0]  

```

```text
 (Document(page\_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state\_of\_the\_union.txt'}),  
 0.802509746274066)  

```

## Retriever options[​](#retriever-options "Direct link to Retriever options")

This section goes over different options for how to use SupabaseVectorStore as a retriever.

### Maximal Marginal Relevance Searches[​](#maximal-marginal-relevance-searches "Direct link to Maximal Marginal Relevance Searches")

In addition to using similarity search in the retriever object, you can also use `mmr`.

```python
retriever = vector\_store.as\_retriever(search\_type="mmr")  

```

```python
matched\_docs = retriever.get\_relevant\_documents(query)  

```

```python
for i, d in enumerate(matched\_docs):  
 print(f"\n## Document {i}\n")  
 print(d.page\_content)  

```

```text
   
 ## Document 0  
   
 Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections.   
   
 Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.   
   
 One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.   
   
 And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.  
   
 ## Document 1  
   
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
   
 ## Document 2  
   
 And I’m taking robust action to make sure the pain of our sanctions is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers.   
   
 Tonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.   
   
 America will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.   
   
 These steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming.   
   
 But I want you to know that we are going to be okay.   
   
 When the history of this era is written Putin’s war on Ukraine will have left Russia weaker and the rest of the world stronger.   
   
 While it shouldn’t have taken something so terrible for people around the world to see what’s at stake now everyone sees it clearly.  
   
 ## Document 3  
   
 We can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together.   
   
 I recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera.   
   
 They were responding to a 9-1-1 call when a man shot and killed them with a stolen gun.   
   
 Officer Mora was 27 years old.   
   
 Officer Rivera was 22.   
   
 Both Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers.   
   
 I spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.   
   
 I’ve worked on these issues a long time.   
   
 I know what works: Investing in crime prevention and community police officers who’ll walk the beat, who’ll know the neighborhood, and who can restore trust and safety.  

```

- [Similarity search with score](#similarity-search-with-score)

- [Retriever options](#retriever-options)

  - [Maximal Marginal Relevance Searches](#maximal-marginal-relevance-searches)

- [Maximal Marginal Relevance Searches](#maximal-marginal-relevance-searches)
