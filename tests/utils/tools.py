'''Tests the tools and utilities in pulsar.utils.'''
from pulsar import system, get_actor
from pulsar.utils.tools import checkarity
from pulsar.apps.test import unittest

def f0(a, b):
    pass

def f0_discount(request, a, b):
    pass

def f1(a, b=0):
    pass

def f2(a, **kwargs):
    # This fails curretly
    pass


def arity_check(func, *args, **kwargs):
    discount = kwargs.pop('discount', 0)
    return checkarity(func, args, kwargs, discount=discount)


class TestArityCheck(unittest.TestCase):

    def testArity0(self):
        self.assertEqual(arity_check(f0, 3, 4), None)
        self.assertEqual(arity_check(f0, 3),
                         '"f0" takes 2 parameters. 1 given.')
        self.assertEqual(arity_check(f0),
                         '"f0" takes 2 parameters. 0 given.')
        self.assertEqual(arity_check(f0, 4, 5, 6),
                         '"f0" takes 2 parameters. 3 given.')
        self.assertEqual(arity_check(f0, a=3, b=5),None)
        self.assertEqual(arity_check(f0, a=3, c=5),
                         '"f0" has missing "b" parameter.')
        self.assertEqual(arity_check(f0, a=3, c=5, d=6),
                         '"f0" takes 2 parameters. 3 given.')
        
    def testArity0WidthDiscount(self):
        f0 = f0_discount
        fname = f0.__name__
        self.assertEqual(arity_check(f0, 3, 4, discount=1), None)
        self.assertEqual(arity_check(f0, 3, discount=1),
                         '"%s" takes 2 parameters. 1 given.' % fname)
        self.assertEqual(arity_check(f0, discount=1),
                         '"%s" takes 2 parameters. 0 given.' % fname)
        self.assertEqual(arity_check(f0, 4, 5, 6, discount=1),
                         '"%s" takes 2 parameters. 3 given.' % fname)
        self.assertEqual(arity_check(f0, a=3, b=5, discount=1),None)
        self.assertEqual(arity_check(f0, a=3, c=5, discount=1),
                         '"%s" has missing "b" parameter.' % fname)
        self.assertEqual(arity_check(f0, a=3, c=5, d=6, discount=1),
                         '"%s" takes 2 parameters. 3 given.' % fname)

    def testArity1(self):
        self.assertEqual(checkarity(f1,(3,),{}),None)
        self.assertEqual(checkarity(f1,(3,4),{}),None)
        self.assertEqual(checkarity(f1,(),{}),
                         '"f1" takes at least 1 parameters. 0 given.')
        self.assertEqual(checkarity(f1,(4,5,6),{}),
                         '"f1" takes at most 2 parameters. 3 given.')
        self.assertEqual(checkarity(f1,(),{'a':3,'b':5}),None)
        self.assertEqual(checkarity(f1,(),{'a':3,'c':5}),
                         '"f1" does not accept "c" parameter.')
        self.assertEqual(checkarity(f1,(),{'a':3,'c':5, 'd':6}),
                         '"f1" takes at most 2 parameters. 3 given.')

    def testArity2(self):
        self.assertEqual(checkarity(f2,(3,),{}),None)
        self.assertEqual(checkarity(f2,(3,),{'c':4}),None)
        self.assertEqual(checkarity(f2,(3,4),{}),
                         '"f2" takes 1 positional parameters. 2 given.')
        self.assertEqual(checkarity(f2,(),{}),
                         '"f2" takes at least 1 parameters. 0 given.')
        self.assertEqual(checkarity(f2,(4,5,6),{}),
                         '"f2" takes 1 positional parameters. 3 given.')
        self.assertEqual(checkarity(f2,(),{'a':3,'b':5}),None)
        self.assertEqual(checkarity(f2,(),{'a':3,'c':5}),None)
        self.assertEqual(checkarity(f2,(),{'b':3,'c':5}),
                         '"f2" has missing "a" parameter.')
        self.assertEqual(checkarity(f2,(),{'a':3,'c':5,'d':6}),None)


class TestSystemInfo(unittest.TestCase):

    def testMe(self):
        worker = get_actor()
        info = system.system_info(worker.pid)
        self.assertTrue(isinstance(info,dict))
