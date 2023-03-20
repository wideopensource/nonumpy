from john import TestCase

from nonumpy import Filter, EMA, Factory


class FactoryTests(TestCase, Factory):
    def test_create_ema(self):
        sut = self.create_FilterLowPassButterworth(
            sample_rate_hz=1, order=2, cutoff_hz=1)

        self.assertTrue(isinstance(sut, Filter))

    def test_create_filter(self):
        sut = self.create_EMA(alpha=0.1)

        self.assertTrue(isinstance(sut, EMA))
