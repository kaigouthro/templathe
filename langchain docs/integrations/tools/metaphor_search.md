# Metaphor Search

Metaphor is a search engine fully designed to be used by LLMs. You can search and then get the contents for any page.

This notebook goes over how to use Metaphor search.

First, you need to set up the proper API keys and environment variables. Get 1000 free searches/month [here](https://platform.metaphor.systems/).

Then enter your API key as an environment variable.

```python
import os  
  
os.environ["METAPHOR\_API\_KEY"] = "..."  

```

## Using their SDK[​](#using-their-sdk "Direct link to Using their SDK")

This is the newer and more supported way to use the Metaphor API - via their SDK

```python
# !pip install metaphor-python  

```

```python
from metaphor\_python import Metaphor  
  
client = Metaphor(api\_key=os.environ["METAPHOR\_API\_KEY"])  

```

```python
from langchain.agents import tool  
from typing import List  

```

```python
@tool  
def search(query: str):  
 """Call search engine with a query."""  
 return client.search(query, use\_autoprompt=True, num\_results=5)  
  
@tool  
def get\_contents(ids: List[str]):  
 """Get contents of a webpage.  
   
 The ids passed in should be a list of ids as fetched from `search`.  
 """  
 return client.get\_contents(ids)  
  
@tool  
def find\_similar(url: str):  
 """Get search results similar to a given URL.  
   
 The url passed in should be a URL returned from `search`  
 """  
 return client.find\_similar(url, num\_results=5)  

```

```python
tools = [search, get\_contents, find\_similar]  

```

### Use in an agent[​](#use-in-an-agent "Direct link to Use in an agent")

```python
from langchain.chat\_models import ChatOpenAI  
llm = ChatOpenAI(temperature=0)  

```

```python
from langchain.agents import OpenAIFunctionsAgent  
from langchain.schema import SystemMessage  
system\_message = SystemMessage(content="You are a web researcher who uses search engines to look up information.")  
prompt = OpenAIFunctionsAgent.create\_prompt(system\_message=system\_message)  
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)  

```

```python
from langchain.agents import AgentExecutor  
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  

```

```python
agent\_executor.run("Find the hottest AI agent startups and what they do")  

```

```text
   
   
 > Entering new AgentExecutor chain...  
   
 Invoking: `search` with `{'query': 'hottest AI agent startups'}`  
   
   
 SearchResponse(results=[Result(title='A Search Engine for Machine Intelligence', url='https://bellow.ai/', id='bdYc6hvHww\_JvLv9k8NhPA', score=0.19460266828536987, published\_date='2023-01-01', author=None, extract=None), Result(title='Adept: Useful General Intelligence', url='https://www.adept.ai/', id='aNBppxBZvQRZMov6sFVj9g', score=0.19103890657424927, published\_date='2000-01-01', author=None, extract=None), Result(title='HiOperator | Generative AI-Enhanced Customer Service', url='https://www.hioperator.com/', id='jieb6sB53mId3EDo0z-SDw', score=0.18549954891204834, published\_date='2000-01-01', author=None, extract=None), Result(title='Home - Stylo', url='https://www.askstylo.com/', id='kUiCuCjJYMD4N0NXdCtqlQ', score=0.1837376356124878, published\_date='2000-01-01', author=None, extract=None), Result(title='DirectAI', url='https://directai.io/?utm\_source=twitter&utm\_medium=raw\_message&utm\_campaign=first\_launch', id='45iSS8KnJ9tL1ilPg3dL9A', score=0.1835256814956665, published\_date='2023-01-01', author=None, extract=None), Result(title='Sidekick AI | Customer Service Automated', url='https://www.sidekickai.co/', id='nCoPMUtqWQqhUvsdTjJT6A', score=0.18215584754943848, published\_date='2020-01-01', author=None, extract=None), Result(title='Hebbia - Search, Reinvented', url='https://www.hebbia.ai/', id='Zy0YaekZdd4rurPQKkys7A', score=0.1799020767211914, published\_date='2023-01-01', author=None, extract=None), Result(title='AI.XYZ', url='https://www.ai.xyz/', id='A5c1ePEvsaQeml2Kui\_-vA', score=0.1797989457845688, published\_date='2023-01-01', author=None, extract=None), Result(title='Halist AI', url='https://halist.ai/', id='-lKPLSb4N4dgMZlTgoDvJg', score=0.17975398898124695, published\_date='2023-03-01', author=None, extract=None), Result(title='Clone your best expert', url='https://airin.ai/', id='\_XIjx1YLPfI4cKePIEc\_bQ', score=0.17957791686058044, published\_date='2016-02-12', author=None, extract=None)], api=<metaphor\_python.api.Metaphor object at 0x104192140>)  
 Invoking: `get\_contents` with `{'ids': ['bdYc6hvHww\_JvLv9k8NhPA', 'aNBppxBZvQRZMov6sFVj9g', 'jieb6sB53mId3EDo0z-SDw', 'kUiCuCjJYMD4N0NXdCtqlQ', '45iSS8KnJ9tL1ilPg3dL9A', 'nCoPMUtqWQqhUvsdTjJT6A', 'Zy0YaekZdd4rurPQKkys7A', 'A5c1ePEvsaQeml2Kui\_-vA', '-lKPLSb4N4dgMZlTgoDvJg', '\_XIjx1YLPfI4cKePIEc\_bQ']}`  
   
   
 GetContentsResponse(contents=[DocumentContent(id='bdYc6hvHww\_JvLv9k8NhPA', url='https://bellow.ai/', title='A Search Engine for Machine Intelligence', extract="<div><div><h2>More Opinions</h2><p>Get responses from multiple AIs</p><p>Don't rely on a single source of truth, explore the full space of machine intelligence and get highly tailored results.</p></div></div>"), DocumentContent(id='aNBppxBZvQRZMov6sFVj9g', url='https://www.adept.ai/', title='Adept: Useful General Intelligence', extract='<div><div><p>Useful <br />General <br />Intelligence</p></div>'), DocumentContent(id='jieb6sB53mId3EDo0z-SDw', url='https://www.hioperator.com/', title='HiOperator | Generative AI-Enhanced Customer Service', extract="<div><div><div><div><div><h2>Generative AI-Enhanced Customer Support Automation</h2><p>Flexible, Scalable Customer Support</p></div><div><p></p></div></div><p></p></div><div><div><p>Why HiOperator?</p><h2>Truly scalable customer service</h2><p>A digital-first customer service provider that changes all the rules of what's possible. Scalable. 100% US-Based. Effortless. HiOperator is the digital payoff.</p></div><p></p></div><div><div><p>Next-Gen Customer Service</p><h2>Scaling with HiOperator's Superagents</h2><p>HiOperator is only possible in the digital era. Our revolutionary software connects with your systems to empower our agents to learn quickly and deliver incredible accuracy. </p></div><div><div><p></p><div><h3>Train Us Once</h3><p>We handle all of the recruiting, hiring, and training moving forward. Never have to deal with another classroom retraining or head count headaches.</p></div></div><div><div><h3>Send Us Tickets</h3><p>We pull tickets automatically from your preferred CRM vendor into our custom system. You have full control over <strong>how</strong> and <strong>when</strong> we get tickets.</p></div><p></p></div><div><p></p><div><h3>Pay per resolution</h3><p>We charge for each conversation we solve. No onboarding fees. No hourly rates. Pay for what you use.</p></div></div></div></div><div><p>Customer Experience</p><h2>Insights &amp;Â\xa0News</h2></div><div><div><h2>Let's transform your customer service.</h2><p>We can onboard in a matter of days and we offer highly flexible contracts. Whether you need a large team to handle your support or some overflow assistance, getting started is easy.</p></div><p>We can onboard in a matter of days and we offer highly flexible contracts. Whether you need a large team to handle your support or some overflow assistance, getting started is easy.</p></div></div>"), DocumentContent(id='kUiCuCjJYMD4N0NXdCtqlQ', url='https://www.askstylo.com/', title='Home - Stylo', extract='<div><div><header><div><p></p><h2>Stop angry customers from breaking support</h2><p></p></div></header><div><p></p><h2><em> </em><strong><em>â\x80\x9cWe solve 99 tickets perfectly </em>ð\x9f\x98\x87<em> but the 1 we miss lands in the CEOâ\x80\x99s inbox </em>ð\x9f\x98«<em>â\x80\x9d<br /></em></strong></h2><p></p><div><p><strong>â\x80\x8d</strong>That 1 costly ticket breaks your process, metrics, and the will of your team. Angry customers make support teams less effective, which makes customers angrier in return.<strong><br />â\x80\x8d</strong><br />Stylo is AI that tells you where to most effectively spend your time to improve the customer experience. This leads to happier customers, employees, and reduces churn.</p><p>â\x80\x8d<strong>No setup, no learning curve, just plug it in and go.</strong></p></div></div><div><div><p></p><div><p>â\x80\x9cIâ\x80\x99m able to better manage the team because I can pinpoint gaps in the teamâ\x80\x99s knowledge or training, and find room for process improvements.â\x80\x9d</p><p></p></div></div></div></div>'), DocumentContent(id='45iSS8KnJ9tL1ilPg3dL9A', url='https://directai.io/?utm\_source=twitter&utm\_medium=raw\_message&utm\_campaign=first\_launch', title='DirectAI', extract="<div><div><div><h2>Vision models without training data.<br /></h2><p>Build and deploy powerful computer vision models with plain language.<br />No code or training required.</p></div><div><h2>Fundamentally different.</h2><p>We use large language models and zero-shot learning to instantly build models that fit your description.</p><br /></div><div><div><p></p><h2>We're removing the last major barrier to creating custom models - <br />training data.</h2><p></p></div><div><table><colgroup></colgroup><thead><tr><th><p>Deploy and iterate in seconds with DirectAI</p></th></tr></thead><tbody><tr><td>• Don't spend time assembling training data.</td></tr><tr><td>• Don't pay a third party to label your data.</td></tr><tr><td>• Don't pay to train your model.</td></tr><tr><td>• Don't spend months finetuning your model's behavior.</td></tr></tbody></table></div></div><div><h2>Venture-backed.<p>Based in NYC.</p><p>We're changing how people use AI in the real world.</p><p>Come talk to us on .</p></h2></div></div></div>"), DocumentContent(id='nCoPMUtqWQqhUvsdTjJT6A', url='https://www.sidekickai.co/', title='Sidekick AI | Customer Service Automated', extract='<div><div><div><div><div><div><div><p>Hi, I am an AI named Jenny, working at Pizza Planet. How can I help you today?</p></div><div><p>How much are large pizzas with 1 topping?</p></div><div><p>For most toppings, a large with one topping would be $10.99.</p></div><div><p>Ok, can I order a large with pepperoni</p></div><div><p>Sure! Takeout or delivery?</p></div><div><p>Alright, order placed. See you at 5 pm!</p></div></div><div><p></p></div></div><p></p></div><div><p>Meet Sidekick</p><div><p>\n Sidekick is an AI agent built to hold natural and dynamic conversations with your customers and talk just like a human.</p><p>Built on the world\'s most advanced AI models, Sidekick pushes the state of the art in natural conversation and converses seamlessly with your customers.\n </p></div><p>Try it out ➜</p><p>Try it out ↓</p></div><div><p>An AI agent designed for <strong>service-led growth.</strong></p><div><div><p></p><p>Personal</p><p>Every customer is different, and has unique needs. Our agents are built to provide personalized service depending on the customer\'s needs.</p></div><div><p></p><p>Fast</p><p>Unlike humans, our Sidekicks respond near-instantly, any time of the day. Your customers won\'t wait for service ever again.</p></div><div><p></p><p>Effective</p><p>Customers love great service, and Sidekick delivers. Grow revenue by solving issues in minutes instead of hours, and providing personalized support to each customer.</p></div></div></div><div><p>Integrating with <strong>your tools.</strong></p></div><div><p><strong>Wherever </strong>your customers are.</p><p>\n Sidekick takes an omnichannel approach to customer service, aggregating all customer interactions across all platforms in one area. Currently most social media platforms are supported, along with website embeddings and API integration.\n </p><div><div><div><p>On the web.</p><div><p>Sidekick makes adding a live chat to your website as simple as copy and pasting a single line of code.</p><p>Chat bubbles discretely sit in the bottom right corner and provide a smooth conversation experience, with AI and human agents alike.</p></div></div><p></p><p></p></div><div><div><p>On Facebook.</p><div><p>Sidekick integrates with your Facebook pages to make live customer service one click away.</p><p>Customers can reach your agent and get service without ever leaving Messenger.</p></div></div><p></p><p></p></div><div><div><p>On Instagram.</p><div><p>E-Commerce on Instagram is especially demanding for customer service.</p><p>Sidekick integrates easily with Instagram accounts to put a live agent one click away.</p></div></div><p></p><p></p></div><div><div><p>On Twitter.</p><div><p>Customers are spending more time on Twitter, which means businesses should provide customer service right on the platform.</p><p>Sidekick integrates easily with Twitter accounts to put a live agent one click away.</p></div></div><p></p><p></p></div><div><div><p>Anywhere you want.</p><div><p>Our API provides programmatic access to your Sidekick agent to integrate into your own app.</p><p>We\'ve built simple abstractions over the chat interface to make it easy to work with our API.</p></div></div><div><div><p>Endpoints</p><div><p>POST</p><p>https://www.api.sidekickai.co/converse</p></div></div><div><p>Sample Request</p><div><pre>{\n "access\_token": "KjZUZBWAOKwgLWAlVFyL",\n "conversation\_id": "23874",\n "body": "How much is a large 2 topping?"\n}</pre></div></div><div><p>Sample Response</p><div><pre>{\n "response": "A large'), DocumentContent(id='Zy0YaekZdd4rurPQKkys7A', url='https://www.hebbia.ai/', title='Hebbia - Search, Reinvented', extract="<div><div><h2>Direct to the point <br />with cutting-edge AI.</h2><p>Stop relying on archaic software, traditional Q&amp;A emails, or waiting for deal partners. Get answers on your own time with accuracy that you can't replicate with humans. <br />â\x80\x8d<br /></p><p>HebbiaÂ\xa0retrieves <strong>every</strong> answer, even insights humans overlook. <br /></p></div>"), DocumentContent(id='A5c1ePEvsaQeml2Kui\_-vA', url='https://www.ai.xyz/', title='AI.XYZ', extract='<div><div>\n \n \n<article>\n \n \n \n \n \n<div><div>\n<p><h2><strong>Go be human</strong></h2></p>\n</div><div><p>\n</p><h4>Let your AI deal with the rest</h4>\n<p></p></div><div><p>Design your own AI with AI.XYZ</p></div><div>\n \n \n \n <p></p>\n \n </div></div>\n \n \n \n \n<div><p>\n</p><h3><strong>The digital world was designed to make us more productive but now navigating it all has become its own job.</strong></h3>\n<p></p></div>\n \n \n \n \n<section>\n <div>\n \n \n \n \n \n \n \n \n <p></p>\n \n \n </div>\n <div><div><p>\n</p><h2><strong>Take life a little easier</strong></h2>\n<p></p></div><div>\n \n \n \n <p></p>\n \n </div><div><p>\n</p><h2><strong>Tackles info<br />overload</strong></h2>\n<p></p></div><div><p>\n</p><h4>“Like ChatGPT, but way more proactive and useful because it’s designed by me, for only me”</h4>\n<p></p></div><div>\n \n \n \n <p></p>\n \n </div><div><p>\n</p><h2><strong>Never sits<br />around</strong></h2>\n<p></p></div><div><p>\n</p><h4>“Even if I’m not interacting with it, my AI looks for ways to simplify my day, surprising me with useful ideas”</h4>\n<p></p></div><div>\n \n \n \n <p></p>\n \n </div><div><p>\n</p><h2><strong>Supports and<br />inspires</strong></h2>\n<p></p></div><div><p>\n</p><h4>“It takes things off my plate, but also cheers me on throughout the day — helping me navigate it all”</h4>\n<p></p></div></div>\n \n \n</section>\n \n \n \n \n<div><div><p>\n</p><h2><strong>Create your AI in 3 simple steps:</strong></h2>\n<p></p></div><div>\n<p><strong>STEP ONE</strong></p><h2><strong>Pick a face and voice</strong></h2><h4>Choose from our library of characters or add your own unique face and voice.</h4>\n</div><div>\n \n \n \n <p></p>\n \n </div><div>\n<p><strong>STEP TWO</strong></p><h2><strong>Create your AI’s persona and memory</strong></h2><h4>Decide who your AI is, its purpose and what it will help you with. Paste information that you want your AI to know.</h4>\n</div><div>\n \n \n \n <p></p>\n \n </div><div>\n<p><strong>STEP THREE</strong></p><h2><strong>Get started</strong></h2><h4>Ask your AI to help you with ideas and support throughout your day. Eventually it will be able to proactively support you.</h4>\n</div><div>\n \n \n \n <p></p>\n \n </div></div>\n \n \n \n \n<section>\n <div>\n \n \n \n \n \n \n \n \n <p></p>\n \n \n </div>\n <div><p>\n</p><h2><strong>Start training your AI to do things for you</strong></h2>\n<p></p></div>\n \n \n</section>\n \n</article>\n \n \n \n \n \n </div></div'), DocumentContent(id='-lKPLSb4N4dgMZlTgoDvJg', url='https://halist.ai/', title='Halist AI', extract='<div><div>\n<p><a href="/app/">Start for free</a></p><p>\nPowered by OpenAI GPT-3 and GPT-4.\n</p>\n<h2>ChatGPT. Lightning-fast and private. Everywhere.</h2>\n<h2>Optimized access to the AI on mobile.</h2>\n<p></p><p>\nTo install Halist on <b>iPhone</b>, open the web app in Safari and tap the "Share" icon. Then, tap "Add to Home Screen" and follow the prompts.\nTo install on <b>Android</b>, open the website in Chrome and tap the three dots in the top right corner. Then, tap "Add to Home screen" and follow the prompts.\n</p>\n</div></div>'), DocumentContent(id='\_XIjx1YLPfI4cKePIEc\_bQ', url='https://airin.ai/', title='Clone your best expert', extract='<div><section><section><div><p> Airin clones how your top expert solves problems in as little as 2 hours. Airin creates an AI companion for the rest of your team by focusing on the patterns in your expert’s questions and hypotheses, not their answers. <a href="/how-it-works">Learn how it works </a></p></div></section><section><div><p> Your customers, agents, sales teams, and consultants can independently solve a wider-range of complex problems with an AI companion. This eliminates the need to maintain large teams of specialized experts. </p></div></section><section><div><p> Airin automates remote coaching for new hires and dramatically reduces time to productivity. New employees partner with your AI companion and meet productivity standards in half the time. </p></div></section></section>')])Here are some of the hottest AI agent startups and what they do:  
   
 1. [Bellow AI](https://bellow.ai/): This startup provides a search engine for machine intelligence. It allows users to get responses from multiple AIs, exploring the full space of machine intelligence and getting highly tailored results.  
   
 2. [Adept AI](https://www.adept.ai/): Adept is focused on creating useful general intelligence.  
   
 3. [HiOperator](https://www.hioperator.com/): HiOperator offers generative AI-enhanced customer support automation. It provides scalable, digital-first customer service and uses its software to empower agents to learn quickly and deliver accurate results.  
   
 4. [Stylo](https://www.askstylo.com/): Stylo uses AI to help manage customer support, identifying where to most effectively spend time to improve the customer experience.  
   
 5. [DirectAI](https://directai.io/): DirectAI allows users to build and deploy powerful computer vision models with plain language, without the need for code or training.  
   
 6. [Sidekick AI](https://www.sidekickai.co/): Sidekick AI is built to hold natural and dynamic conversations with customers, providing personalized service depending on the customer's needs.  
   
 7. [Hebbia](https://www.hebbia.ai/): Hebbia is reinventing search with cutting-edge AI, retrieving every answer, even insights humans overlook.  
   
 8. [AI.XYZ](https://www.ai.xyz/): AI.XYZ allows users to design their own AI, tackling information overload and providing support and inspiration throughout the day.  
   
 9. [Halist AI](https://halist.ai/): Halist AI provides optimized access to ChatGPT, powered by OpenAI GPT-3 and GPT-4, on mobile.  
   
 10. [Airin](https://airin.ai/): Airin clones how your top expert solves problems in as little as 2 hours, creating an AI companion for the rest of your team. It automates remote coaching for new hires and dramatically reduces time to productivity.  
   
   
 > Finished chain.  
  
  
  
  
  
 "Here are some of the hottest AI agent startups and what they do:\n\n1. [Bellow AI](https://bellow.ai/): This startup provides a search engine for machine intelligence. It allows users to get responses from multiple AIs, exploring the full space of machine intelligence and getting highly tailored results.\n\n2. [Adept AI](https://www.adept.ai/): Adept is focused on creating useful general intelligence.\n\n3. [HiOperator](https://www.hioperator.com/): HiOperator offers generative AI-enhanced customer support automation. It provides scalable, digital-first customer service and uses its software to empower agents to learn quickly and deliver accurate results.\n\n4. [Stylo](https://www.askstylo.com/): Stylo uses AI to help manage customer support, identifying where to most effectively spend time to improve the customer experience.\n\n5. [DirectAI](https://directai.io/): DirectAI allows users to build and deploy powerful computer vision models with plain language, without the need for code or training.\n\n6. [Sidekick AI](https://www.sidekickai.co/): Sidekick AI is built to hold natural and dynamic conversations with customers, providing personalized service depending on the customer's needs.\n\n7. [Hebbia](https://www.hebbia.ai/): Hebbia is reinventing search with cutting-edge AI, retrieving every answer, even insights humans overlook.\n\n8. [AI.XYZ](https://www.ai.xyz/): AI.XYZ allows users to design their own AI, tackling information overload and providing support and inspiration throughout the day.\n\n9. [Halist AI](https://halist.ai/): Halist AI provides optimized access to ChatGPT, powered by OpenAI GPT-3 and GPT-4, on mobile.\n\n10. [Airin](https://airin.ai/): Airin clones how your top expert solves problems in as little as 2 hours, creating an AI companion for the rest of your team. It automates remote coaching for new hires and dramatically reduces time to productivity.\n"  

```

## Using the tool wrapper[​](#using-the-tool-wrapper "Direct link to Using the tool wrapper")

This is the old way of using Metaphor - through our own in-house integration.

```python
from langchain.utilities import MetaphorSearchAPIWrapper  

```

```python
search = MetaphorSearchAPIWrapper()  

```

### Call the API[​](#call-the-api "Direct link to Call the API")

`results` takes in a Metaphor-optimized search query and a number of results (up to 500). It returns a list of results with title, url, author, and creation date.

```python
search.results("The best blog post about AI safety is definitely this: ", 10)  

```

```text
 [{'title': 'Core Views on AI Safety: When, Why, What, and How',  
 'url': 'https://www.anthropic.com/index/core-views-on-ai-safety',  
 'author': None,  
 'published\_date': '2023-03-08'},  
 {'title': 'Extinction Risk from Artificial Intelligence',  
 'url': 'https://aisafety.wordpress.com/',  
 'author': None,  
 'published\_date': '2013-10-08'},  
 {'title': 'The simple picture on AI safety - LessWrong',  
 'url': 'https://www.lesswrong.com/posts/WhNxG4r774bK32GcH/the-simple-picture-on-ai-safety',  
 'author': 'Alex Flint',  
 'published\_date': '2018-05-27'},  
 {'title': 'No Time Like The Present For AI Safety Work',  
 'url': 'https://slatestarcodex.com/2015/05/29/no-time-like-the-present-for-ai-safety-work/',  
 'author': None,  
 'published\_date': '2015-05-29'},  
 {'title': 'A plea for solutionism on AI safety - LessWrong',  
 'url': 'https://www.lesswrong.com/posts/ASMX9ss3J5G3GZdok/a-plea-for-solutionism-on-ai-safety',  
 'author': 'Jasoncrawford',  
 'published\_date': '2023-06-09'},  
 {'title': 'The Artificial Intelligence Revolution: Part 1 - Wait But Why',  
 'url': 'https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html',  
 'author': 'Tim Urban',  
 'published\_date': '2015-01-22'},  
 {'title': 'Anthropic: Core Views on AI Safety: When, Why, What, and How - EA Forum',  
 'url': 'https://forum.effectivealtruism.org/posts/uGDCaPFaPkuxAowmH/anthropic-core-views-on-ai-safety-when-why-what-and-how',  
 'author': 'Jonmenaster',  
 'published\_date': '2023-03-09'},  
 {'title': "[Linkpost] Sam Altman's 2015 Blog Posts Machine Intelligence Parts 1 & 2 - LessWrong",  
 'url': 'https://www.lesswrong.com/posts/QnBZkNJNbJK9k5Xi7/linkpost-sam-altman-s-2015-blog-posts-machine-intelligence',  
 'author': 'Olivia Jimenez',  
 'published\_date': '2023-04-28'},  
 {'title': 'The Proof of Doom - LessWrong',  
 'url': 'https://www.lesswrong.com/posts/xBrpph9knzWdtMWeQ/the-proof-of-doom',  
 'author': 'Johnlawrenceaspden',  
 'published\_date': '2022-03-09'},  
 {'title': "Anthropic's Core Views on AI Safety - LessWrong",  
 'url': 'https://www.lesswrong.com/posts/xhKr5KtvdJRssMeJ3/anthropic-s-core-views-on-ai-safety',  
 'author': 'Zac Hatfield-Dodds',  
 'published\_date': '2023-03-09'}]  

```

### Adding filters[​](#adding-filters "Direct link to Adding filters")

We can also add filters to our search.

include_domains: Optional\[List\[str\]\] - List of domains to include in the search. If specified, results will only come from these domains. Only one of include_domains and exclude_domains should be specified.

exclude_domains: Optional\[List\[str\]\] - List of domains to exclude in the search. If specified, results will only come from these domains. Only one of include_domains and exclude_domains should be specified.

start_crawl_date: Optional\[str\] - "Crawl date" refers to the date that Metaphor discovered a link, which is more granular and can be more useful than published date. If start_crawl_date is specified, results will only include links that were crawled after start_crawl_date. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

end_crawl_date: Optional\[str\] - "Crawl date" refers to the date that Metaphor discovered a link, which is more granular and can be more useful than published date. If endCrawlDate is specified, results will only include links that were crawled before end_crawl_date. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

start_published_date: Optional\[str\] - If specified, only links with a published date after start_published_date will be returned. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Note that for some links, we have no published date, and these links will be excluded from the results if start_published_date is specified.

end_published_date: Optional\[str\] - If specified, only links with a published date before end_published_date will be returned. Must be specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Note that for some links, we have no published date, and these links will be excluded from the results if end_published_date is specified.

See full docs [here](https://metaphorapi.readme.io/).

```python
search.results(  
 "The best blog post about AI safety is definitely this: ",  
 10,  
 include\_domains=["lesswrong.com"],  
 start\_published\_date="2019-01-01",  
)  

```

### Use Metaphor as a tool[​](#use-metaphor-as-a-tool "Direct link to Use Metaphor as a tool")

Metaphor can be used as a tool that gets URLs that other tools such as browsing tools.

```python
from langchain.agents.agent\_toolkits import PlayWrightBrowserToolkit  
from langchain.tools.playwright.utils import (  
 create\_async\_playwright\_browser, # A synchronous browser is available, though it isn't compatible with jupyter.  
)  
  
async\_browser = create\_async\_playwright\_browser()  
toolkit = PlayWrightBrowserToolkit.from\_browser(async\_browser=async\_browser)  
tools = toolkit.get\_tools()  
  
tools\_by\_name = {tool.name: tool for tool in tools}  
print(tools\_by\_name.keys())  
navigate\_tool = tools\_by\_name["navigate\_browser"]  
extract\_text = tools\_by\_name["extract\_text"]  

```

```python
from langchain.agents import initialize\_agent, AgentType  
from langchain.chat\_models import ChatOpenAI  
from langchain.tools import MetaphorSearchResults  
  
llm = ChatOpenAI(model\_name="gpt-4", temperature=0.7)  
  
metaphor\_tool = MetaphorSearchResults(api\_wrapper=search)  
  
agent\_chain = initialize\_agent(  
 [metaphor\_tool, extract\_text, navigate\_tool],  
 llm,  
 agent=AgentType.STRUCTURED\_CHAT\_ZERO\_SHOT\_REACT\_DESCRIPTION,  
 verbose=True,  
)  
  
agent\_chain.run(  
 "find me an interesting tweet about AI safety using Metaphor, then tell me the first sentence in the post. Do not finish until able to retrieve the first sentence."  
)  

```

- [Using their SDK](#using-their-sdk)

  - [Use in an agent](#use-in-an-agent)

- [Using the tool wrapper](#using-the-tool-wrapper)

  - [Call the API](#call-the-api)
  - [Adding filters](#adding-filters)
  - [Use Metaphor as a tool](#use-metaphor-as-a-tool)

- [Use in an agent](#use-in-an-agent)

- [Call the API](#call-the-api)

- [Adding filters](#adding-filters)

- [Use Metaphor as a tool](#use-metaphor-as-a-tool)
