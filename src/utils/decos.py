class GenLimiter:
    """A decorator used to limit the amount of iterations possible from a generator"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.limit = kwargs.pop("limit", -1)
        self.gen = self.func(*args, **kwargs)
        return self

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self.__call__(instance, *args, **kwargs)
        return wrapper

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit == 0:
            raise StopIteration()
        self.limit -= 1
        return next(self.gen)
