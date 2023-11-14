class Router:
    # existing code...
    def route(self, condition, runnable1, runnable2):
        if condition:
            return runnable1.run()
        else:
            return runnable2.run()