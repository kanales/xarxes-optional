import abc
import numpy as np


class Modulator(abc.ABC):
    def __init__(self, levels, freq=1e4, amplitude=1., samples=20, duration=1):
        """
        The modulator will asume codified inputs to take at most `len(levels)`
        levels and for each of those levels li a modulation value levels[li]
        will be used. Depending on the modulator this could be amplitude, frequency,...
        Parameters
        ----------
        levels : Dict[Int, Float]
            for each possible level li levels[li] contains a value
        freq : float
            base frequency to use when modulating
        amplitude : float
            base amplitude of the modulated wave
        samples : int
            number of (sub)samples per input byte
        duration : float
            default duration of sampling interval
        """
        self.levels = levels
        self.A = amplitude
        self.freq = freq
        self.samples = samples
        self.duration = duration

    @abc.abstractmethod
    def signal(self, xs):
        """
        Given input xs of timesteps generates a signal
        response for each level in `self.levels`

        Parameters
        ----------
        xs : numpy.array
            time steps where the signal is sampled

        Returns
        -------
        Dict[int, numpy.array]
            Dictionary with signal responses for each level
        """
        pass

    def modulate(self, seq, duration=None):
        """
        Parameters
        ----------
        seq : numpy.array
            sequence to modulate
        samples : int
            number of times each bit is sampled
        duration : float
            duration of the sample interval

        Returns
        -------
        (numpy.array, numpy.array)
            modulated sequence, sampling interval
        """
        duration = duration or self.duration
        xs = np.linspace(0, duration, self.samples * len(seq))
        seq = np.repeat(seq, self.samples)
        signals = self.signal(xs)

        ys = np.empty_like(xs)
        for k, signal in signals.items():
            idxs = seq == k
            ys[idxs] = signal[idxs]
        return ys, xs

    def demodulate(self, seq, xs):
        """
        Parameters
        ----------
        seq : numpy.array
            sequence to modulate
        xs : numpy.array
            times where the sequence was sampled

        Returns
        -------
        numpy.array
            demodulated sequence
        """
        signals = self.signal(xs)
        keys = np.array(list(signals.keys()))
        vals = np.array(list(signals.values()))
        # calculate estimated value for each sample
        out_sample = keys[np.abs(vals - seq).argmin(axis=0)]
        return np.median(out_sample.reshape((-1, self.samples)), axis=1).ravel().astype(int)


class DefaultModulator(Modulator):
    def signal(self, xs):
        return {
            k: np.ones_like(xs) * x for k, x in self.levels.items()
        }


class ASKModulator(Modulator):

    def signal(self, xs):
        return {
            k: a * np.cos(2*np.pi * self.freq * xs) for k, a in self.levels.items()
        }


class FSKModulator(Modulator):

    def signal(self, xs):
        freqs = self.levels
        return {
            k: self.A * np.cos(2*np.pi * f * xs) for k, f in self.levels.items()
        }


class PSKModulator(Modulator):

    def signal(self, xs):
        return {
            k: self.A * np.cos(2*np.pi * self.freq * xs + off) for k, off in self.levels.items()
        }
