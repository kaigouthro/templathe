# Cookbook

Example code for accomplishing common tasks with the LangChain Expression Language (LCEL). These examples show how to compose different Runnable (the core LCEL interface) components to achieve various tasks. If you're just getting acquainted with LCEL, the [Prompt + LLM](/docs/expression_language/cookbook/prompt_llm_parser) page is a good place to start.

## 📄️ Prompt + LLM

The most common and valuable composition is taking:

## 📄️ RAG

Let's look at adding in a retrieval step to a prompt and LLM, which adds up to a "retrieval-augmented generation" chain

## 📄️ Multiple chains

Runnables can easily be used to string together multiple Chains

## 📄️ Querying a SQL DB

We can replicate our SQLDatabaseChain with Runnables.

## 📄️ Agents

You can pass a Runnable into an agent.

## 📄️ Code writing

Example of how to use LCEL to write Python code.

## 📄️ Adding memory

This shows how to add memory to an arbitrary chain. Right now, you can use the memory classes but need to hook it up manually

## 📄️ Adding moderation

This shows how to add in moderation (or other safeguards) around your LLM application.

## 📄️ Using tools

You can use any Tools with Runnables easily.
