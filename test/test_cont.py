import unittest

from funcy import identity

from OldSeaMap.cont import Cont


class ContTestCase(unittest.TestCase):
    def test_monad(self):
        self.assertEqual(Cont.of(5).bind(lambda x: Cont.of(x + 2)).run(identity), 7)

    def test_call_cc(self):
        def cond(k, a, b):
            return a if k else b

        func = (lambda x: Cont.call_cc(
            lambda exit1: (
                cond(x == 'e1', exit1('exited from exit1'), Cont.call_cc(
                    lambda exit2: (
                        cond(x == 'e2', exit2('exited from exit2'), Cont.of('exited from end'))))))))
        self.assertEqual(Cont.of(5)
                         .bind(lambda x: Cont.call_cc(lambda exit1: exit1(-1) if x == 5 else Cont.of(5)))
                         .run(identity), -1)
        self.assertEqual(Cont.of(4)
                         .bind(lambda x: Cont.call_cc(lambda exit1: exit1(-1) if x == 5 else Cont.of(5)))
                         .run(identity), 5)
        self.assertEqual(Cont.of('e1').bind(func).run(identity), 'exited from exit1')
        self.assertEqual(Cont.of('e2').bind(func).run(identity), 'exited from exit2')
        self.assertEqual(Cont.of('e0').bind(func).run(identity), 'exited from end')

    def test_functor(self):
        self.assertEqual(Cont.of(5).map(lambda x: x / 5), Cont.of(1))

    def test_applicative(self):
        self.assertEqual(Cont.of(5).ap(Cont.of(lambda x: x / 5)), Cont.of(1))


if __name__ == '__main__':
    unittest.main()
