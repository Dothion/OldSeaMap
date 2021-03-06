import unittest

from funcy import partial

from OldSeaMap.maybe import Just, NOTHING


def safe_div(x, y):
    return NOTHING if y == 0 else Just(x / y)


class MaybeTestCase(unittest.TestCase):
    def test_functor(self):
        self.assertEqual(Just(5).map(lambda x: x / 5), Just(1))
        self.assertEqual(Just(5).map(lambda x: x / 5), Just(1))
        self.assertEqual(NOTHING.map(lambda x: x / 0), NOTHING)
        self.assertRaises(ZeroDivisionError, Just(5).map, lambda x: x / 0)

    def test_applicative(self):
        self.assertEqual(Just(5).ap(Just.of(lambda x: x / 5)), Just(1))
        self.assertEqual(Just(5).ap(NOTHING), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(lambda x: x / 5)), NOTHING)
        self.assertEqual(NOTHING.ap(Just.of(NOTHING)), NOTHING)
        self.assertEqual(Just(lambda x: x / 5).ap_with(Just.of(5)), Just(1))
        self.assertEqual(Just.lift_a(lambda x: x * 2)(5), Just(10))
        self.assertEqual(Just.lift_a(2)(lambda x, y: x / y)(5)(5), Just(1))
        self.assertRaises(ZeroDivisionError, Just(5).ap, Just.of(lambda x: x / 0))
        self.assertRaises(ZeroDivisionError, Just.lift_a(2)(lambda x, y: x / y)(5), 0)

    def test_monad(self):
        self.assertEqual(Just(5).bind(partial(safe_div, y=5)), Just(1))
        self.assertEqual(Just(5).bind(partial(safe_div, y=0)), NOTHING)
        self.assertEqual(NOTHING.bind(partial(safe_div, y=5)), NOTHING)
        self.assertEqual(NOTHING.bind(partial(safe_div, y=0)), NOTHING)

    def test_monoid(self):
        # self.assertEqual(Just(5).append(Just(3)), Just(5))
        # self.assertEqual(Just(3).append(Just(5)), Just(3))
        # self.assertEqual(NOTHING.append(Just(3)), Just(3))
        # self.assertEqual(Just(3).append(NOTHING), Just(3))
        ...


if __name__ == '__main__':
    unittest.main()
