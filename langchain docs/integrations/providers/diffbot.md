# Diffbot

[Diffbot](https://docs.diffbot.com/docs) is a service to read web pages. Unlike traditional web scraping tools,
`Diffbot` doesn't require any rules to read the content on a page.
It starts with computer vision, which classifies a page into one of 20 possible types. Content is then interpreted by a machine learning model trained to identify the key attributes on a page based on its type.
The result is a website transformed into clean-structured data (like JSON or CSV), ready for your application.

## Installation and Setup[​](#installation-and-setup "Direct link to Installation and Setup")

Read [instructions](https://docs.diffbot.com/reference/authentication) how to get the Diffbot API Token.

## Document Loader[​](#document-loader "Direct link to Document Loader")

See a [usage example](/docs/integrations/document_loaders/diffbot).

```python
from langchain.document\_loaders import DiffbotLoader  

```

- [Installation and Setup](#installation-and-setup)
- [Document Loader](#document-loader)
