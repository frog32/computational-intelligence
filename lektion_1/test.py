import unittest

from ea import Fass


class TestConversion(unittest.TestCase):
    def test_h_and_d(self):
        test_values = (
            (0, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (5, 3, [0, 0, 1, 0, 1, 0, 0, 0, 1, 1]),
            (28, 23, [1, 1, 1, 0, 0, 1, 0, 1, 1, 1]),
        )
        for d, h, seq in test_values:
            fass = Fass(seq)
            self.assertEqual(fass.h, h)
            self.assertEqual(fass.d, d)


class TestFitness(unittest.TestCase):
    def test_nb_max(self):
        f = Fass([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertAlmostEqual(f.fitness, 4528.605810149687)
        self.assertEqual(f.is_valid, True)

    def test_nb_min(self):
        f = Fass([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertAlmostEqual(f.fitness, 0.0)
        self.assertEqual(f.is_valid, False)


if __name__ == '__main__':
    unittest.main()
