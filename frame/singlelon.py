class Singleton(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]
"""
#python2
class MyClass(BaseClass):
        __metaclass__ = Singleton
#python3
class MyClass(BaseClass, metaclass = Singleton):
"""


