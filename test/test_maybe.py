import unittest

from funcy import curry

from OldSeaMap.maybe import Just, NOTHING

divide_by_zero = curry(lambda x: x / 0)
divide_by_five = curry(lambda x: x / 5)
just_five = Just(5)


class MaybeTestCase(unittest.TestCase):
    def test_functor(self):
        self.assertEqual(just_five.map(divide_by_five), Just(1))
        self.assertEqual(NOTHING.map(divide_by_zero), NOTHING)
        self.assertEqual(just_five.map(divide_by_zero), NOTHING)

    def test_applicative(self):
        self.assertEqual(just_five.ap(Just.of(divide_by_five)), Just(1))
        self.assertEqual(just_five.ap(Just.of(divide_by_zero)), NOTHING)
        self.assertEqual(just_five.ap(divide_by_five), NotImplemented)
        self.assertEqual(just_five.ap(NOTHING), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(divide_by_five)), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(NOTHING)), NOTHING)

    def test_monad(self):
        ...

    def test_monoid(self):
        ...


if __name__ == '__main__':
    unittest.main()
