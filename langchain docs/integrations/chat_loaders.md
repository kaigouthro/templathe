# Chat loaders

## 📄️ Discord

This notebook shows how to create your own chat loader that works on copy-pasted messages (from dms) to a list of LangChain messages.

## 📄️ Facebook Messenger

This notebook shows how to load data from Facebook in a format you can fine-tune on. The overall steps are:

## 📄️ GMail

This loader goes over how to load data from GMail. There are many ways you could want to load data from GMail. This loader is currently fairly opinionated in how to do so. The way it does it is it first looks for all messages that you have sent. It then looks for messages where you are responding to a previous email. It then fetches that previous email, and creates a training example of that email, followed by your email.

## 📄️ iMessage

This notebook shows how to use the iMessage chat loader. This class helps convert iMessage conversations to LangChain chat messages.

## 📄️ Fine-Tuning on LangSmith Chat Datasets

This notebook demonstrates an easy way to load a LangSmith chat dataset fine-tune a model on that data.

## 📄️ Fine-Tuning on LangSmith LLM Runs

This notebook demonstrates how to directly load data from LangSmith's LLM runs and fine-tune a model on that data.

## 📄️ Slack

This notebook shows how to use the Slack chat loader. This class helps map exported slack conversations to LangChain chat messages.

## 📄️ Telegram

This notebook shows how to use the Telegram chat loader. This class helps map exported Telegram conversations to LangChain chat messages.

## 📄️ Twitter (via Apify)

This notebook shows how to load chat messages from Twitter to fine-tune on. We do this by utilizing Apify.

## 📄️ WeChat

There is not yet a straightforward way to export personal WeChat messages. However if you just need no more than few hundreds of messages for model fine-tuning or few-shot examples, this notebook shows how to create your own chat loader that works on copy-pasted WeChat messages to a list of LangChain messages.

## 📄️ WhatsApp

This notebook shows how to use the WhatsApp chat loader. This class helps map exported WhatsApp conversations to LangChain chat messages.
