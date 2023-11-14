class Pipeline:
    def __init__(self):
        self.functions = []
        self.generators = []

    def add_function(self, func):
        self.functions.append(func)

    def add_generator(self, generator):
        self.generators.append(generator)

    def run_functions(self, input_data):
        for func in self.functions:
            input_data = func(input_data)
        return input_data

    def run_generators(self, input_data):
        for generator in self.generators:
            input_data = generator(input_data)
        return input_data