# How to

## 📄️ Async API

LangChain provides async support for Chains by leveraging the asyncio library.

## 📄️ Different call methods

All classes inherited from Chain offer a few ways of running chain logic. The most direct one is by using call:

## 📄️ Custom chain

To implement your own custom chain you can subclass Chain and implement the following methods:

## 📄️ Debugging chains

It can be hard to debug a Chain object solely from its output as most Chain objects involve a fair amount of input prompt preprocessing and LLM output post-processing.

## 📄️ Loading from LangChainHub

This notebook covers how to load chains from LangChainHub.

## 📄️ Adding memory (state)

Chains can be initialized with a Memory object, which will persist data across calls to the chain. This makes a Chain stateful.

## 📄️ Using OpenAI functions

This walkthrough demonstrates how to incorporate OpenAI function-calling API's in a chain. We'll go over:

## 📄️ Serialization

This notebook covers how to serialize chains to and from disk. The serialization format we use is JSON or YAML. Currently, only some chains support this type of serialization. We will grow the number of supported chains over time.
