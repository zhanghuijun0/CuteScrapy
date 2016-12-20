def test_args_kwargs(arg1, arg2, arg3):
    print "arg1:", arg1
    print "arg2:", arg2
    print "arg3:", arg3


import pdb
def make_bread():
    pdb.set_trace()
    return "I don't have time"


def generator_function():
    for i in range(10):
        yield i
        print 'item:%s' % i
# for item in generator_function():
#     print(item)




def fibon1(n):
    a = b = 1
    result = []
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result


# for i in fibon1(10000):
#     print i


# generator version
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b
# for x in fibon(100000000):
#     print 1

from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func1(x):
   """Do some math."""
   return x + x


# result = addition_func1(4)
# print result




