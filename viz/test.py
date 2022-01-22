import sys


def one():
    return "one"


def two():
    return "two"


def test(x):
    switcher = {
        '1': one(),
        '2': two()
    }
    return switcher.get(x, "nothing")

print(sys.argv[1])
print(test(sys.argv[1]))