import unittest

from funcy import partial

from OldSeaMap.result import Ok, Err

ERR = Err('error')


def safe_div(x, y):
    return Err('Divide by zero') if y == 0 else Ok(x / y)


class ResultTestCase(unittest.TestCase):
    def test_functor(self):
        self.assertEqual(Ok(5).map(lambda x: x / 5), Ok(1))
        self.assertEqual(Ok(5).map(lambda x: x / 5), Ok(1))
        self.assertIsInstance(Ok(5).map(lambda x: x / 0), Err)
        self.assertIsInstance(ERR.map(lambda x: x / 0), Err)

    def test_applicative(self):
        self.assertEqual(Ok(5).ap(Ok.of(lambda x: x / 5)), Ok(1))
        self.assertIsInstance(Ok(5).ap(Ok.of(lambda x: x / 0)), Err)
        self.assertEqual(Ok(5).ap(ERR), ERR)
        self.assertEqual(ERR.ap(Ok.of(lambda x: x / 5)), ERR)
        self.assertEqual(ERR.ap(Ok.of(ERR)), ERR)
        self.assertEqual(Ok(lambda x: x / 5).ap_with(Ok.of(5)), Ok(1))
        self.assertEqual(Ok.lift_a(lambda x: x * 2)(5), Ok(10))
        self.assertEqual(Ok.lift_a(2)(lambda x, y: x / y)(5)(5), Ok(1))
        self.assertIsInstance(Ok.lift_a(2)(lambda x, y: x / y)(5)(0), Err)

    def test_monad(self):
        self.assertEqual(Ok(5).bind(partial(safe_div, y=5)), Ok(1))
        self.assertEqual(Ok(5).bind(partial(safe_div, y=0)), Err('Divide by zero'))
        self.assertEqual(ERR.bind(partial(safe_div, y=5)), ERR)
        self.assertEqual(ERR.bind(partial(safe_div, y=0)), ERR)


if __name__ == '__main__':
    unittest.main()
