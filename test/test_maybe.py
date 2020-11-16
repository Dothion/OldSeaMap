import unittest
from OldSeaMap.maybe import Just, NOTHING
from funcy import curry


class MaybeTestCase(unittest.TestCase):
    def test_functor(self):
        divide_by_zero = curry(lambda x: x / 0)
        divide_by_five = curry(lambda x: x / 5)
        just_five = Just(5)
        nothing = NOTHING

        self.assertEqual(just_five.map(divide_by_five), Just(1))


if __name__ == '__main__':
    unittest.main()
