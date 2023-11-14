class RunnableParallel:
    def __init__(self, runnables):
        self.runnables = runnables

    def run(self):
        return {runnable.name: runnable.run() for runnable in self.runnables}