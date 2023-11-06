# Reddit

[Reddit](https://www.reddit.com) is an American social news aggregation, content rating, and discussion website.

This loader fetches the text from the Posts of Subreddits or Reddit users, using the `praw` Python package.

Make a [Reddit Application](https://www.reddit.com/prefs/apps/) and initialize the loader with with your Reddit API credentials.

```python
from langchain.document\_loaders import RedditPostsLoader  

```

```python
# !pip install praw  

```

```python
# load using 'subreddit' mode  
loader = RedditPostsLoader(  
 client\_id="YOUR CLIENT ID",  
 client\_secret="YOUR CLIENT SECRET",  
 user\_agent="extractor by u/Master\_Ocelot8179",  
 categories=["new", "hot"], # List of categories to load posts from  
 mode="subreddit",  
 search\_queries=[  
 "investing",  
 "wallstreetbets",  
 ], # List of subreddits to load posts from  
 number\_posts=20, # Default value is 10  
)  
  
# # or load using 'username' mode  
# loader = RedditPostsLoader(  
# client\_id="YOUR CLIENT ID",  
# client\_secret="YOUR CLIENT SECRET",  
# user\_agent="extractor by u/Master\_Ocelot8179",  
# categories=['new', 'hot'],  
# mode = 'username',  
# search\_queries=['ga3far', 'Master\_Ocelot8179'], # List of usernames to load posts from  
# number\_posts=20  
# )  
  
# Note: Categories can be only of following value - "controversial" "hot" "new" "rising" "top"  

```

```python
documents = loader.load()  
documents[:5]  

```

```text
 [Document(page\_content='Hello, I am not looking for investment advice. I will apply my own due diligence. However, I am interested if anyone knows as a UK resident how fees and exchange rate differences would impact performance?\n\nI am planning to create a pie of index funds (perhaps UK, US, europe) or find a fund with a good track record of long term growth at low rates. \n\nDoes anyone have any ideas?', metadata={'post\_subreddit': 'r/investing', 'post\_category': 'new', 'post\_title': 'Long term retirement funds fees/exchange rate query', 'post\_score': 1, 'post\_id': '130pa6m', 'post\_url': 'https://www.reddit.com/r/investing/comments/130pa6m/long\_term\_retirement\_funds\_feesexchange\_rate\_query/', 'post\_author': Redditor(name='Badmanshiz')}),  
 Document(page\_content='I much prefer the Roth IRA and would rather rollover my 401k to that every year instead of keeping it in the limited 401k options. But if I rollover, will I be able to continue contributing to my 401k? Or will that close my account? I realize that there are tax implications of doing this but I still think it is the better option.', metadata={'post\_subreddit': 'r/investing', 'post\_category': 'new', 'post\_title': 'Is it possible to rollover my 401k every year?', 'post\_score': 3, 'post\_id': '130ja0h', 'post\_url': 'https://www.reddit.com/r/investing/comments/130ja0h/is\_it\_possible\_to\_rollover\_my\_401k\_every\_year/', 'post\_author': Redditor(name='AnCap\_Catholic')}),  
 Document(page\_content='Have a general question? Want to offer some commentary on markets? Maybe you would just like to throw out a neat fact that doesn\'t warrant a self post? Feel free to post here! \n\nIf your question is "I have $10,000, what do I do?" or other "advice for my personal situation" questions, you should include relevant information, such as the following:\n\n\* How old are you? What country do you live in? \n\* Are you employed/making income? How much? \n\* What are your objectives with this money? (Buy a house? Retirement savings?) \n\* What is your time horizon? Do you need this money next month? Next 20yrs? \n\* What is your risk tolerance? (Do you mind risking it at blackjack or do you need to know its 100% safe?) \n\* What are you current holdings? (Do you already have exposure to specific funds and sectors? Any other assets?) \n\* Any big debts (include interest rate) or expenses? \n\* And any other relevant financial information will be useful to give you a proper answer. \n\nPlease consider consulting our FAQ first - https://www.reddit.com/r/investing/wiki/faq\nAnd our [side bar](https://www.reddit.com/r/investing/about/sidebar) also has useful resources. \n\nIf you are new to investing - please refer to Wiki - [Getting Started](https://www.reddit.com/r/investing/wiki/index/gettingstarted/)\n\nThe reading list in the wiki has a list of books ranging from light reading to advanced topics depending on your knowledge level. Link here - [Reading List](https://www.reddit.com/r/investing/wiki/readinglist)\n\nCheck the resources in the sidebar.\n\nBe aware that these answers are just opinions of Redditors and should be used as a starting point for your research. You should strongly consider seeing a registered investment adviser if you need professional support before making any financial decisions!', metadata={'post\_subreddit': 'r/investing', 'post\_category': 'new', 'post\_title': 'Daily General Discussion and Advice Thread - April 27, 2023', 'post\_score': 5, 'post\_id': '130eszz', 'post\_url': 'https://www.reddit.com/r/investing/comments/130eszz/daily\_general\_discussion\_and\_advice\_thread\_april/', 'post\_author': Redditor(name='AutoModerator')}),  
 Document(page\_content="Based on recent news about salt battery advancements and the overall issues of lithium, I was wondering what would be feasible ways to invest into non-lithium based battery technologies? CATL is of course a choice, but the selection of brokers I currently have in my disposal don't provide HK stocks at all.", metadata={'post\_subreddit': 'r/investing', 'post\_category': 'new', 'post\_title': 'Investing in non-lithium battery technologies?', 'post\_score': 2, 'post\_id': '130d6qp', 'post\_url': 'https://www.reddit.com/r/investing/comments/130d6qp/investing\_in\_nonlithium\_battery\_technologies/', 'post\_author': Redditor(name='-manabreak')}),  
 Document(page\_content='Hello everyone,\n\nI would really like to invest in an ETF that follows spy or another big index, as I think this form of investment suits me best. \n\nThe problem is, that I live in Denmark where ETFs and funds are taxed annually on unrealised gains at quite a steep rate. This means that an ETF growing say 10% per year will only grow about 6%, which really ruins the long term effects of compounding interest.\n\nHowever stocks are only taxed on realised gains which is why they look more interesting to hold long term.\n\nI do not like the lack of diversification this brings, as I am looking to spend tonnes of time picking the right long term stocks.\n\nIt would be ideal to find a few stocks that over the long term somewhat follows the indexes. Does anyone have suggestions?\n\nI have looked at Nasdaq Inc. which quite closely follows Nasdaq 100. \n\nI really appreciate any help.', metadata={'post\_subreddit': 'r/investing', 'post\_category': 'new', 'post\_title': 'Stocks that track an index', 'post\_score': 7, 'post\_id': '130auvj', 'post\_url': 'https://www.reddit.com/r/investing/comments/130auvj/stocks\_that\_track\_an\_index/', 'post\_author': Redditor(name='LeAlbertP')})]  

```
