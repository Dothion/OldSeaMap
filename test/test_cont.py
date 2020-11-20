import unittest

from funcy import identity

from OldSeaMap.cont import Cont


class ContTestCase(unittest.TestCase):
    def test_monad(self):
        self.assertEqual(Cont.of(5).bind(lambda x: Cont.of(x + 2)).run(identity), 7)

    def test_call_cc(self):
        def cond(k, a, b):  # No short circuit eval. Only used for demonstration.
            return a if k else b

        func = (lambda x: Cont.call_cc(
            lambda exit1: (
                cond(x == 1, exit1((x + 1, 'exit1')), Cont.call_cc(
                    lambda exit2: (
                        cond(x == 2, exit2((x * 2, 'exit2')), Cont.of((x - 3, 'end')))))))))
        safe_div = (lambda y: lambda x: Cont.call_cc(
            lambda err: (err('Error: Divide by zero.') if y == 0 else Cont.of(x / y))))
        self.assertEqual(Cont.of(5)
                         .bind(lambda x: Cont.call_cc(lambda exit1: exit1(-1) if x == 5 else Cont.of(5)))
                         .run(identity), -1)
        self.assertEqual(Cont.of(4)
                         .bind(lambda x: Cont.call_cc(lambda exit1: exit1(-1) if x == 5 else Cont.of(5)))
                         .run(identity), 5)
        self.assertEqual(Cont.of(1).bind(func).run(identity), (2, 'exit1'))
        self.assertEqual(Cont.of(2).bind(func).run(identity), (4, 'exit2'))
        self.assertEqual(Cont.of(3).bind(func).run(identity), (0, 'end'))
        self.assertEqual(Cont.of(5).bind(safe_div(5)).run(identity), 1)
        self.assertEqual(Cont.of(5).bind(safe_div(0)).run(identity), 'Error: Divide by zero.')

    def test_functor(self):
        self.assertEqual(Cont.of(5).map(lambda x: x / 5), Cont.of(1))

    def test_applicative(self):
        self.assertEqual(Cont.of(5).ap(Cont.of(lambda x: x / 5)), Cont.of(1))


if __name__ == '__main__':
    unittest.main()
