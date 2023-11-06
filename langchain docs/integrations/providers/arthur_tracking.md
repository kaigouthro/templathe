# Arthur

[Arthur](https://arthur.ai) is a model monitoring and observability platform.

The following guide shows how to run a registered chat LLM with the Arthur callback handler to automatically log model inferences to Arthur.

If you do not have a model currently onboarded to Arthur, visit our [onboarding guide for generative text models](https://docs.arthur.ai/user-guide/walkthroughs/model-onboarding/generative_text_onboarding.html). For more information about how to use the Arthur SDK, visit our [docs](https://docs.arthur.ai/).

```python
from langchain.callbacks import ArthurCallbackHandler  
from langchain.callbacks.streaming\_stdout import StreamingStdOutCallbackHandler  
from langchain.chat\_models import ChatOpenAI  
from langchain.schema import HumanMessage  

```

Place Arthur credentials here

```python
arthur\_url = "https://app.arthur.ai"  
arthur\_login = "your-arthur-login-username-here"  
arthur\_model\_id = "your-arthur-model-id-here"  

```

Create Langchain LLM with Arthur callback handler

```python
def make\_langchain\_chat\_llm(chat\_model=):  
 return ChatOpenAI(  
 streaming=True,  
 temperature=0.1,  
 callbacks=[  
 StreamingStdOutCallbackHandler(),  
 ArthurCallbackHandler.from\_credentials(  
 arthur\_model\_id,   
 arthur\_url=arthur\_url,   
 arthur\_login=arthur\_login)  
 ])  

```

```python
chatgpt = make\_langchain\_chat\_llm()  

```

```text
 Please enter password for admin: ········  

```

Running the chat LLM with this `run` function will save the chat history in an ongoing list so that the conversation can reference earlier messages and log each response to the Arthur platform. You can view the history of this model's inferences on your [model dashboard page](https://app.arthur.ai/).

Enter `q` to quit the run loop

```python
def run(llm):  
 history = []  
 while True:  
 user\_input = input("\n>>> input >>>\n>>>: ")  
 if user\_input == "q":  
 break  
 history.append(HumanMessage(content=user\_input))  
 history.append(llm(history))  

```

```python
run(chatgpt)  

```

```text
   
 >>> input >>>  
 >>>: What is a callback handler?  
 A callback handler, also known as a callback function or callback method, is a piece of code that is executed in response to a specific event or condition. It is commonly used in programming languages that support event-driven or asynchronous programming paradigms.  
   
 The purpose of a callback handler is to provide a way for developers to define custom behavior that should be executed when a certain event occurs. Instead of waiting for a result or blocking the execution, the program registers a callback function and continues with other tasks. When the event is triggered, the callback function is invoked, allowing the program to respond accordingly.  
   
 Callback handlers are commonly used in various scenarios, such as handling user input, responding to network requests, processing asynchronous operations, and implementing event-driven architectures. They provide a flexible and modular way to handle events and decouple different components of a system.  
 >>> input >>>  
 >>>: What do I need to do to get the full benefits of this  
 To get the full benefits of using a callback handler, you should consider the following:  
   
 1. Understand the event or condition: Identify the specific event or condition that you want to respond to with a callback handler. This could be user input, network requests, or any other asynchronous operation.  
   
 2. Define the callback function: Create a function that will be executed when the event or condition occurs. This function should contain the desired behavior or actions you want to take in response to the event.  
   
 3. Register the callback function: Depending on the programming language or framework you are using, you may need to register or attach the callback function to the appropriate event or condition. This ensures that the callback function is invoked when the event occurs.  
   
 4. Handle the callback: Implement the necessary logic within the callback function to handle the event or condition. This could involve updating the user interface, processing data, making further requests, or triggering other actions.  
   
 5. Consider error handling: It's important to handle any potential errors or exceptions that may occur within the callback function. This ensures that your program can gracefully handle unexpected situations and prevent crashes or undesired behavior.  
   
 6. Maintain code readability and modularity: As your codebase grows, it's crucial to keep your callback handlers organized and maintainable. Consider using design patterns or architectural principles to structure your code in a modular and scalable way.  
   
 By following these steps, you can leverage the benefits of callback handlers, such as asynchronous and event-driven programming, improved responsiveness, and modular code design.  
 >>> input >>>  
 >>>: q  

```
