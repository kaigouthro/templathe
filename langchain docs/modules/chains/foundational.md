# Foundational

## 📄️ LLM

The most common type of chaining in any LLM application is combining a prompt template with an LLM and optionally an output parser.

## 📄️ Router

Routing allows you to create non-deterministic chains where the output of a previous step defines the next step. Routing helps provide structure and consistency around interactions with LLMs.

## 📄️ Sequential

The next step after calling a language model is to make a series of calls to a language model. This is particularly useful when you want to take the output from one call and use it as the input to another.

## 📄️ Transformation

Often we want to transform inputs as they are passed from one component to another.
