# Sequential

The next step after calling a language model is to make a series of calls to a language model. This is particularly useful when you want to take the output from one call and use it as the input to another.

The recommended way to do this is using the LangChain Expression Language. The legacy way is using the `SequentialChain`, which we continue to document here for backwards compatibility.

As a toy example, let's suppose we want to create a chain that first creates a play synopsis and then generates a play review based on the synopsis.

```python
from langchain.prompts import PromptTemplate  
  
synopsis\_prompt = PromptTemplate.from\_template(  
 """You are a playwright. Given the title of play, it is your job to write a synopsis for that title.  
  
Title: {title}  
Playwright: This is a synopsis for the above play:"""  
)  
  
review\_prompt = PromptTemplate.from\_template(  
 """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.  
  
Play Synopsis:  
{synopsis}  
Review from a New York Times play critic of the above play:"""  
)  

```

## Using LCEL[​](#using-lcel "Direct link to Using LCEL")

Creating a sequence of calls (to LLMs or any other component/arbitrary function) is precisely what LangChain Expression Language was designed for.

```python
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import StrOutputParser  
  
llm = ChatOpenAI()  
chain = {"synopsis": synopsis\_prompt | llm | StrOutputParser()} | review\_prompt | llm | StrOutputParser()  
chain.invoke({"title": "Tragedy at sunset on the beach"})  

```

```text
 'In "Tragedy at Sunset on the Beach," playwright has crafted a deeply affecting drama that delves into the complexities of human relationships and the consequences that arise from one fateful evening. Set against the breathtaking backdrop of a serene beach at sunset, the play takes audiences on an emotional journey as it explores the lives of four individuals whose paths intertwine in unexpected and tragic ways.\n\nAt the center of the story is Sarah, a young woman grappling with the recent loss of her husband. Seeking solace and a fresh start, she embarks on a solitary trip to the beach, hoping to find peace and clarity. It is here that she encounters James, a charismatic but troubled artist, lost in his own world of anguish and self-doubt. The unlikely connection they form becomes the catalyst for a series of heart-wrenching events, as their emotional baggage and personal demons collide.\n\nThe play skillfully weaves together the narratives of Sarah, James, and Rachel, Sarah\'s best friend. As Rachel arrives on the beach with the intention of helping Sarah heal, she unknowingly carries a secret that threatens to shatter their friendship forever. Against the backdrop of crashing waves and vibrant sunsets, the characters\' lives unravel, exposing hidden desires, betrayals, and deeply buried secrets. The boundaries of love, friendship, and loyalty blur, forcing each character to confront their own vulnerabilities and face the consequences of their choices.\n\nWhat sets "Tragedy at Sunset on the Beach" apart is its ability to evoke genuine emotion from its audience. The playwright\'s poignant exploration of the human condition touches upon universal themes of loss, forgiveness, and the lengths we go to protect the ones we love. The richly drawn characters come alive on stage, their struggles and triumphs resonating deeply with the audience. Moments of intense emotion are skillfully crafted, leaving spectators captivated and moved.\n\nThe play\'s evocative setting adds another layer of depth to the storytelling. The picturesque beach at sunset becomes a metaphor for the fragility of life and the fleeting nature of happiness. The crashing waves and vibrant colors serve as a backdrop to the characters\' unraveling lives, heightening the emotional impact of their stories.\n\nWhile "Tragedy at Sunset on the Beach" is undeniably a heavy and somber play, it ultimately leaves audiences questioning the power of redemption. The characters\' journeys, though tragic, offer glimpses of hope and the potential for healing. It reminds us that even amidst the darkest moments, there is still a chance for redemption and forgiveness.\n\nOverall, "Tragedy at Sunset on the Beach" is a thought-provoking and emotionally charged play that will captivate audiences from start to finish. The playwright\'s skillful storytelling, evocative setting, and richly drawn characters make for a truly memorable theatrical experience. This is a play that will leave spectators questioning their own lives and the choices they make, long after the curtain falls.'  

```

If we wanted to get back the synopsis as well we could do:

```python
from langchain.schema.runnable import RunnablePassthrough  
  
synopsis\_chain = synopsis\_prompt | llm | StrOutputParser()   
review\_chain = review\_prompt | llm | StrOutputParser()  
chain = {"synopsis": synopsis\_chain} | RunnablePassthrough.assign(review=review\_chain)  
chain.invoke({"title": "Tragedy at sunset on the beach"})  

```

```text
 {'synopsis': 'Tragedy at Sunset on the Beach is a gripping and emotionally charged drama that delves into the complexities of human relationships and the fragility of life. Set against the backdrop of a picturesque beach at sunset, the play follows a group of friends who gather to celebrate a joyous occasion.\n\nAs the sun begins its descent, tensions simmer beneath the surface, and long-held secrets and resentments come to light. The characters find themselves entangled in a web of love, betrayal, and loss, as they confront their deepest fears and desires.\n\nThe main focus revolves around Sarah, a vibrant and free-spirited woman who becomes the center of a tragic event. Through a series of flashback scenes, we witness the unraveling of her life, exploring her complicated relationships with her closest friends and romantic partners.\n\nThe play explores themes of regret, redemption, and the consequences of our choices. It delves into the human condition, questioning the nature of happiness and the value of time. The audience is taken on an emotional rollercoaster, experiencing moments of laughter, heartache, and profound reflection.\n\nTragedy at Sunset on the Beach challenges conventional notions of tragedy, evoking a sense of empathy and understanding for the flawed and vulnerable characters. It serves as a reminder that life is unpredictable and fragile, urging us to cherish every moment and embrace the beauty that exists even amidst tragedy.',  
 'review': "In Tragedy at Sunset on the Beach, playwright John Smithson delivers a powerful and thought-provoking exploration of the human experience. Set against the stunning backdrop of a beach at sunset, this emotionally charged drama takes the audience on a journey through the complexities of relationships, the fragility of life, and the profound impact of our choices.\n\nSmithson skillfully weaves together a tale of love, betrayal, and loss, as a group of friends gather to celebrate a joyous occasion. As the sun sets, tensions rise, and long-held secrets and resentments are exposed, leaving the characters entangled in a web of emotions. Through a series of poignant flashback scenes, we witness the unraveling of Sarah's life, a vibrant and free-spirited woman who becomes the center of a tragic event.\n\nWhat sets Tragedy at Sunset on the Beach apart is its ability to challenge conventional notions of tragedy. Smithson masterfully portrays flawed and vulnerable characters with such empathy and understanding that the audience can't help but empathize with their struggles. This play serves as a reminder that life is unpredictable and fragile, urging us to cherish every moment and embrace the beauty that exists even amidst tragedy.\n\nThe performances in this production are nothing short of extraordinary. The actors effortlessly navigate the emotional rollercoaster of the script, eliciting moments of laughter, heartache, and profound reflection from the audience. Their ability to convey the complexities of their characters' relationships and inner turmoil is truly commendable.\n\nThe direction by Jane Anderson is impeccable, capturing the essence of the beach at sunset and utilizing the space to create an immersive experience for the audience. The use of flashbacks adds depth and nuance to the narrative, allowing for a deeper understanding of the characters and their motivations.\n\nTragedy at Sunset on the Beach is not a play for the faint of heart. It tackles heavy themes of regret, redemption, and the consequences of our choices. However, it is precisely this raw and unflinching exploration of the human condition that makes it such a compelling piece of theater. Smithson's writing, combined with the exceptional performances and direction, make this play a must-see for theatergoers looking for a thought-provoking and emotionally resonant experience.\n\nIn a city renowned for its theater scene, Tragedy at Sunset on the Beach stands out as a shining example of the power of live performance to evoke empathy, provoke contemplation, and remind us of the fragile beauty of life. It is a production that will linger in the minds and hearts of its audience long after the final curtain falls."}  

```

Head to the [LCEL](/docs/expression_language) section for more on the interface, built-in features, and cookbook examples.

## \[Legacy\] SequentialChain[​](#legacy-sequentialchain "Direct link to legacy-sequentialchain")

Sequential chains allow you to connect multiple chains and compose them into pipelines that execute some specific scenario. There are two types of sequential chains:

- `SimpleSequentialChain`: The simplest form of sequential chains, where each step has a singular input/output, and the output of one step is the input to the next.
- `SequentialChain`: A more general form of sequential chains, allowing for multiple inputs/outputs.

### SimpleSequentialChain[​](#simplesequentialchain "Direct link to SimpleSequentialChain")

```python
from langchain.llms import OpenAI  
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
  
# This is an LLMChain to write a synopsis given a title of a play.  
llm = OpenAI(temperature=.7)  
synopsis\_chain = LLMChain(llm=llm, prompt=synopsis\_prompt)  

```

```python
# This is an LLMChain to write a review of a play given a synopsis.  
llm = OpenAI(temperature=.7)  
review\_chain = LLMChain(llm=llm, prompt=review\_prompt)  

```

```python
# This is the overall chain where we run these two chains in sequence.  
from langchain.chains import SimpleSequentialChain  
  
overall\_chain = SimpleSequentialChain(chains=[synopsis\_chain, review\_chain], verbose=True)  
  
review = overall\_chain.run("Tragedy at sunset on the beach")  

```

```text
   
   
 > Entering new SimpleSequentialChain chain...  
   
   
 Tragedy at Sunset on the Beach is a modern tragedy about a young couple in love. The couple, Jack and Jill, are deeply in love and plan to spend the day together on the beach at sunset. However, when they arrive, they are shocked to discover that the beach is an abandoned, dilapidated wasteland. With no one else around, they explore the beach and start to reminisce about their relationship and the good times they’ve shared.   
   
 But then, out of the blue, a mysterious figure emerges from the shadows and reveals a dark secret. The figure tells the couple that the beach is no ordinary beach, but is in fact the site of a terrible tragedy that took place many years ago. As the figure explains what happened, Jack and Jill become overwhelmed with grief.   
   
 In the end, Jack and Jill are forced to confront the truth about the tragedy and its consequences. The play is ultimately a reflection on the power of tragedy and the human capacity to confront and overcome it.  
   
   
 Tragedy at Sunset on the Beach is a powerful, thought-provoking modern tragedy that is sure to leave a lasting impression on its audience. The play follows the story of Jack and Jill, a young couple deeply in love, as they explore an abandoned beach and discover a dark secret from the past.  
   
 The play brilliantly captures the raw emotions of Jack and Jill as they learn of the tragedy that has occurred on the beach. The writing is masterful, and the actors do a wonderful job of conveying the couple’s grief and pain. The play is ultimately a reflection on the power of tragedy and the human capacity to confront and overcome it.  
   
 Overall, Tragedy at Sunset on the Beach is a must-see for anyone looking for a thought-provoking and emotionally moving play. This play is sure to stay with its audience long after the curtain closes. Highly recommended.  
   
 > Finished chain.  

```

```python
print(review)  

```

```text
   
   
 Tragedy at Sunset on the Beach is a powerful, thought-provoking modern tragedy that is sure to leave a lasting impression on its audience. The play follows the story of Jack and Jill, a young couple deeply in love, as they explore an abandoned beach and discover a dark secret from the past.  
   
 The play brilliantly captures the raw emotions of Jack and Jill as they learn of the tragedy that has occurred on the beach. The writing is masterful, and the actors do a wonderful job of conveying the couple’s grief and pain. The play is ultimately a reflection on the power of tragedy and the human capacity to confront and overcome it.  
   
 Overall, Tragedy at Sunset on the Beach is a must-see for anyone looking for a thought-provoking and emotionally moving play. This play is sure to stay with its audience long after the curtain closes. Highly recommended.  

```

### SequentialChain[​](#sequentialchain "Direct link to SequentialChain")

Of course, not all sequential chains will be as simple as passing a single string as an argument and getting a single string as output for all steps in the chain. In this next example, we will experiment with more complex chains that involve multiple inputs, and where there also multiple final outputs.

Of particular importance is how we name the input/output variables. In the above example we didn't have to think about that because we were just passing the output of one chain directly as input to the next, but here we do have worry about that because we have multiple inputs.

```python
# This is an LLMChain to write a synopsis given a title of a play and the era it is set in.  
llm = OpenAI(temperature=.7)  
synopsis\_template = """You are a playwright. Given the title of play and the era it is set in, it is your job to write a synopsis for that title.  
  
Title: {title}  
Era: {era}  
Playwright: This is a synopsis for the above play:"""  
synopsis\_prompt\_template = PromptTemplate(input\_variables=["title", "era"], template=synopsis\_template)  
synopsis\_chain = LLMChain(llm=llm, prompt=synopsis\_prompt\_template, output\_key="synopsis")  

```

```python
# This is an LLMChain to write a review of a play given a synopsis.  
llm = OpenAI(temperature=.7)  
template = """You are a play critic from the New York Times. Given the synopsis of play, it is your job to write a review for that play.  
  
Play Synopsis:  
{synopsis}  
Review from a New York Times play critic of the above play:"""  
prompt\_template = PromptTemplate(input\_variables=["synopsis"], template=template)  
review\_chain = LLMChain(llm=llm, prompt=prompt\_template, output\_key="review")  
  
# This is the overall chain where we run these two chains in sequence.  
from langchain.chains import SequentialChain  
overall\_chain = SequentialChain(  
 chains=[synopsis\_chain, review\_chain],  
 input\_variables=["era", "title"],  
 # Here we return multiple variables  
 output\_variables=["synopsis", "review"],  
 verbose=True)  
  
  
overall\_chain({"title":"Tragedy at sunset on the beach", "era": "Victorian England"})  

```

```text
   
   
 > Entering new SequentialChain chain...  
   
 > Finished chain.  
  
  
  
  
  
 {'title': 'Tragedy at sunset on the beach',  
 'era': 'Victorian England',  
 'synopsis': "\n\nThe play is set in Victorian England and follows the story of a young couple, Mary and John, who were deeply in love and had just gotten engaged. On the night of their engagement, they decided to take a romantic walk along the beach at sunset. Unexpectedly, John is shot by a stranger and killed right in front of Mary. In a state of shock and anguish, Mary is left alone, struggling to comprehend what has just occurred. \n\nThe play follows Mary as she searches for answers to John's death. As Mary's investigation begins, she discovers that John was actually involved in a dark and dangerous plot to overthrow the government. Unbeknownst to Mary, John had been working as a spy in a secret mission to uncover the truth behind a political scandal. \n\nNow, Mary must face the consequences of her beloved's actions and find a way to save the future of England. As the story unfolds, Mary must confront her own beliefs as well as the powerful people who are determined to end her mission. \n\nAt the end of the play, all of Mary's questions are answered and she is able to make a choice that will ultimately decide the fate of the nation. Tragedy at Sunset on the Beach is a",  
 'review': "\n\nSet against the backdrop of Victorian England, Tragedy at Sunset on the Beach tells a heart-wrenching story of love, loss, and tragedy. The play follows Mary and John, a young couple deeply in love, who experience an unexpected tragedy on the night of their engagement. When John is shot and killed by a stranger, Mary is left alone to uncover the truth behind her beloved's death.\n\nWhat follows is an intense and gripping journey as Mary discovers that John was a spy in a secret mission to uncover a powerful political scandal. As Mary faces off against those determined to end her mission, she must confront her own beliefs and ultimately decide the fate of the nation.\n\nThe play is skillfully crafted and brilliantly performed. The actors portray a range of emotions from joy to sorrow that will leave the audience moved and captivated. The production is a beautiful testament to the power of love and the strength of the human spirit, and it is sure to leave a lasting impression. Highly recommended."}  

```

#### Memory in Sequential Chains[​](#memory-in-sequential-chains "Direct link to Memory in Sequential Chains")

Sometimes you may want to pass along some context to use in each step of the chain or in a later part of the chain, but maintaining and chaining together the input/output variables can quickly get messy. Using `SimpleMemory` is a convenient way to do manage this and clean up your chains.

For example, using the previous playwright `SequentialChain`, lets say you wanted to include some context about date, time and location of the play, and using the generated synopsis and review, create some social media post text. You could add these new context variables as `input_variables`, or we can add a `SimpleMemory` to the chain to manage this context:

```python
from langchain.chains import SequentialChain  
from langchain.memory import SimpleMemory  
  
llm = OpenAI(temperature=.7)  
template = """You are a social media manager for a theater company. Given the title of play, the era it is set in, the date,time and location, the synopsis of the play, and the review of the play, it is your job to write a social media post for that play.  
  
Here is some context about the time and location of the play:  
Date and Time: {time}  
Location: {location}  
  
Play Synopsis:  
{synopsis}  
Review from a New York Times play critic of the above play:  
{review}  
  
Social Media Post:  
"""  
prompt\_template = PromptTemplate(input\_variables=["synopsis", "review", "time", "location"], template=template)  
social\_chain = LLMChain(llm=llm, prompt=prompt\_template, output\_key="social\_post\_text")  
  
overall\_chain = SequentialChain(  
 memory=SimpleMemory(memories={"time": "December 25th, 8pm PST", "location": "Theater in the Park"}),  
 chains=[synopsis\_chain, review\_chain, social\_chain],  
 input\_variables=["era", "title"],  
 # Here we return multiple variables  
 output\_variables=["social\_post\_text"],  
 verbose=True)  
  
overall\_chain({"title":"Tragedy at sunset on the beach", "era": "Victorian England"})  

```

```text
   
   
 > Entering new SequentialChain chain...  
   
 > Finished chain.  
  
  
  
  
  
 {'title': 'Tragedy at sunset on the beach',  
 'era': 'Victorian England',  
 'time': 'December 25th, 8pm PST',  
 'location': 'Theater in the Park',  
 'social\_post\_text': "Experience a heartbreaking love story this Christmas as we bring you 'Tragedy at Sunset on the Beach', set in Victorian England on December 25th at 8pm PST at the Theater in the Park. Follow the story of two young lovers, George and Mary, and their fight against overwhelming odds. Will their love prevail? Find out this Christmas Day! #TragedyAtSunset #LoveStory #Christmas #VictorianEngland"}  

```

- [Using LCEL](#using-lcel)
- [Legacy SequentialChain](#legacy-sequentialchain)
