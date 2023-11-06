# LLMChain

You can use the existing LLMChain in a very similar way to before - provide a prompt and a model.

```python
chain = LLMChain(llm=chat, prompt=chat\_prompt)  

```

```python
chain.run(input\_language="English", output\_language="French", text="I love programming.")  

```

```text
 "J'adore la programmation."  

```
