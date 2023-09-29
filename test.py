def n():
    yield 1


s = n()

print(next(s))
