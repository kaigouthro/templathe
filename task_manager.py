from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions

def execute_task(task):
    agent_executor = AgentExecutor(agent=task, tools=[], verbose=True)
    return agent_executor.execute()

def manage_tasks(tasks):
    results = []
    for task in tasks:
        result = execute_task(task)
        results.append(result)
    return results
