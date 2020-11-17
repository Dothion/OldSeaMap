import unittest

from funcy import curry, partial

from OldSeaMap.maybe import Just, NOTHING


def safe_div(x, y):
    try:
        return Just(x / y)
    except ZeroDivisionError:
        return NOTHING


divide_by_zero = curry(lambda x: x / 0)
divide_by_five = curry(lambda x: x / 5)
just_five = Just(5)
just_three = just_five.replace_with(3)


class MaybeTestCase(unittest.TestCase):
    def test_functor(self):
        self.assertEqual(just_five.map(divide_by_five), Just(1))
        self.assertEqual(NOTHING.map(divide_by_zero), NOTHING)
        self.assertEqual(just_five.map(divide_by_zero), NOTHING)

    def test_applicative(self):
        self.assertEqual(Just(5).ap(Just.of(divide_by_five)), Just(1))
        self.assertEqual(Just(5).ap(Just.of(divide_by_zero)), NOTHING)
        self.assertEqual(Just(5).ap(NOTHING), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(divide_by_five)), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(NOTHING)), NOTHING)

    def test_monad(self):
        self.assertEqual(Just(5).bind(partial(safe_div, y=5)), Just(1))
        self.assertEqual(Just(5).bind(partial(safe_div, y=0)), NOTHING)
        self.assertEqual(NOTHING.bind(partial(safe_div, y=5)), NOTHING)
        self.assertEqual(NOTHING.bind(partial(safe_div, y=0)), NOTHING)

    def test_monoid(self):
        self.assertEqual(Just(5).append(Just(3)), Just(5))
        self.assertEqual(Just(3).append(Just(5)), Just(3))
        self.assertEqual(NOTHING.append(Just(3)), Just(3))
        self.assertEqual(Just(3).append(NOTHING), Just(3))


if __name__ == '__main__':
    unittest.main()
