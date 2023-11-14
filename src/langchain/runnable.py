class Runnable:
    def __init__(self):
        self.constant_args = None
        self.constant_kwargs = None

    def bind(self, *args, **kwargs):
        # existing code...
        self.constant_args = args
        self.constant_kwargs = kwargs