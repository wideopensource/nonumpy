import numpy as np
import matplotlib.pyplot as plt
import nonumpy as nnp


def chirp(number_of_samples: int, min_hz: float, max_hz: float):
    # hacked up from https://udel.edu/~mm/gr/chirp.py
    t_s = np.linspace(0, 1, number_of_samples)  # Chirp sample times.

    c = max_hz - min_hz  # Chirp rate in Hz/s.
    phi_Hz = (c * t_s**2) / 2 + (min_hz * t_s)  # Instantaneous phase.
    phi_rad = 2 * np.pi * phi_Hz  # Convert to radians.
    return t_s, np.exp(1j * phi_rad)


class Tester:
    def __init__(self, number_of_samples=10000, min_hz=10, max_hz=500):
        self.number_of_samples = number_of_samples
        self.min_hz = min_hz
        self.max_hz = max_hz

        T, C = chirp(number_of_samples=number_of_samples,
                     min_hz=min_hz, max_hz=max_hz)

        self.X = T * (max_hz - min_hz) + min_hz
        self.C = C

    def test(self, filter):
        Y = [filter.run(float(a)) for a in self.C]

        plt.plot(self.X, Y)


tester = Tester()

tester.test(nnp.Factory().create_FilterLowPassButterworth(
    sample_rate_hz=tester.number_of_samples, order=10, cutoff_hz=400))

tester.test(nnp.Factory().create_FilterHighPassButterworth(
    sample_rate_hz=tester.number_of_samples, order=2, cutoff_hz=400))

tester.test(nnp.Factory().create_EMA(alpha=0.1))

plt.show()
