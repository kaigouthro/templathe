# Chains

Using an LLM in isolation is fine for simple applications, but more complex applications require chaining LLMs - either with each other or with other components.

LangChain provides two high-level frameworks for "chaining" components. The legacy approach is to use the `Chain` interface. The updated approach is to use the [LangChain Expression Language (LCEL)](/docs/expression_language/). When building new applications we recommend using LCEL for chain composition. But there are a number of useful, built-in `Chain`'s that we continue to support, so we document both frameworks here. As we'll touch on below, `Chain`'s can also themselves be used in LCEL, so the two are not mutually exclusive.

## LCEL[​](#lcel "Direct link to LCEL")

The most visible part of LCEL is that it provides an intuitive and readable syntax for composition. But more importantly, it also provides first-class support for:

- [streaming](/docs/expression_language/interface#stream),
- [async calls](/docs/expression_language/interface#async-stream),
- [batching](/docs/expression_language/interface#batch),
- [parallelization](/docs/expression_language/interface#parallelism),
- retries,
- [fallbacks](/docs/expression_language/how_to/fallbacks),
- tracing,
- [and more.](/docs/expression_language/why)

As a simple and common example, we can see what it's like to combine a prompt, model and output parser:

```python
from langchain.chat\_models import ChatAnthropic  
from langchain.prompts import ChatPromptTemplate  
from langchain.schema import StrOutputParser  
  
model = ChatAnthropic()  
prompt = ChatPromptTemplate.from\_messages([  
 ("system", "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions."),  
 ("human", "{question}"),  
])  
runnable = prompt | model | StrOutputParser()  

```

```python
for chunk in runnable.stream({"question": "How did Mansa Musa accumulate his wealth?"}):  
 print(chunk, end="", flush=True)  

```

```text
 Mansa Musa was the emperor of the Mali Empire in West Africa during the 14th century. He accumulated immense wealth through several means:  
   
 - Gold mining - Mali contained very rich gold deposits, especially in the region of Bambuk. Gold mining and gold trade was a major source of wealth for the empire.  
   
 - Control of trade routes - Mali dominated the trans-Saharan trade routes connecting West Africa to North Africa and beyond. By taxing the goods that passed through its territory, Mali profited greatly.  
   
 - Tributary states - Many lands surrounding Mali paid tribute to the empire. This came in the form of gold, slaves, and other valuable resources.  
   
 - Agriculture - Mali also had extensive agricultural lands irrigated by the Niger River. Surplus food produced could be sold or traded.   
   
 - Royal monopolies - The emperor claimed monopoly rights over the production and sale of certain goods like salt from the Taghaza mines. This added to his personal wealth.  
   
 - Inheritance - As an emperor, Mansa Musa inherited a wealthy state. His predecessors had already consolidated lands and accumulated riches which fell to Musa.  
   
 So in summary, mining, trade, taxes,  

```

For more head to the [LCEL section](/docs/expression_language/).

## \[Legacy\] `Chain` interface[​](#legacy-chain-interface "Direct link to legacy-chain-interface")

**Chain**'s are the legacy interface for "chained" applications. We define a Chain very generically as a sequence of calls to components, which can include other chains. The base interface is simple:

```python
class Chain(BaseModel, ABC):  
 """Base interface that all chains should implement."""  
  
 memory: BaseMemory  
 callbacks: Callbacks  
  
 def \_\_call\_\_(  
 self,  
 inputs: Any,  
 return\_only\_outputs: bool = False,  
 callbacks: Callbacks = None,  
 ) -> Dict[str, Any]:  
 ...  

```

We can recreate the LCEL runnable we made above using the built-in `LLMChain`:

```python
from langchain.chains import LLMChain  
  
  
chain = LLMChain(llm=model, prompt=prompt, output\_parser=StrOutputParser())  
chain.run(question="How did Mansa Musa accumulate his wealth?")  

```

```text
 " Mansa Musa was the emperor of the Mali Empire in West Africa in the early 14th century. He accumulated his vast wealth through several means:\n\n- Gold mining - Mali contained very rich gold deposits, especially in the southern part of the empire. Gold mining and trade was a major source of wealth.\n\n- Control of trade routes - Mali dominated the trans-Saharan trade routes connecting West Africa to North Africa and beyond. By taxing and controlling this lucrative trade, Mansa Musa reaped great riches.\n\n- Tributes from conquered lands - The Mali Empire expanded significantly under Mansa Musa's rule. As new lands were conquered, they paid tribute to the mansa in the form of gold, salt, and slaves.\n\n- Inheritance - Mansa Musa inherited a wealthy empire from his predecessor. He continued to build the wealth of Mali through the factors above.\n\n- Sound fiscal management - Musa is considered to have managed the empire and its finances very effectively, including keeping taxes reasonable and promoting a robust economy. This allowed him to accumulate and maintain wealth.\n\nSo in summary, conquest, trade, taxes, mining, and inheritance all contributed to Mansa Musa growing the M"  

```

For more specifics check out:

- [How-to](/docs/modules/chains/how_to/) for walkthroughs of different chain features

- [Foundational](/docs/modules/chains/foundational/) to get acquainted with core building block chains

- [Document](/docs/modules/chains/document/) to learn how to incorporate documents into chains

- [LCEL](#lcel)

- [Legacy `Chain` interface](#legacy-chain-interface)
