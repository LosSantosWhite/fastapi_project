from functools import wraps


def my_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Вызван декоратор")
        return func(*args, **kwargs)

    return wrapper


class A:
    table = "A"

    @my_dec
    def print(self):
        print(f"Вызван {self.__class__.__name__} == {self.table}")


class B(A):
    table = "B"


b = B()

b.print()
