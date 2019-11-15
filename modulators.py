import abc
import numpy as np

class Modulator(abc.ABC):
    def __init__(self, levels, *args, **kwargs):
        """
        The modulator will asume codified inputs to take at most `len(levels)`
        levels and for each of those levels li a modulation value levels[li]
        will be used. Depending on the modulator this could be amplitude, frequency,...
        Parameters
        ----------
        levels : Dict[Int, Float]
            for each possible level li levels[li] contains a value
        """
        self.levels = levels
        self.A = kwargs.get('amplitude', 1)
        self.freq = kwargs.get('freq', 2e3)

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
    
    def modulate(self, seq, xs):
        """
        Parameters
        ----------
        seq : numpy.array
            sequence to modulate
            
        Returns
        -------
        numpy.array
            modulated sequence
        """
        sample_size = len(xs) // len(seq)
        seq = np.repeat(seq, sample_size)
        pad = len(xs) - len(seq)
        seq = np.pad(seq, (0, pad), 'constant', constant_values=0)
        signals = self.signal(xs)

        ys = np.empty_like(xs)
        for k, signal in signals.items():
            idxs = seq == k
            ys[idxs] = signal[idxs]
        if pad: ys[-pad:] = 0
        return ys

class DefaultModulator(Modulator):
    def signal(self, xs):
        return {
            k: np.ones_like(xs) * x for k,x in self.levels.items()
        }

class ASKModulator(Modulator):

    def signal(self, xs):
        return { 
            k: a * np.cos(2*np.pi *self.freq * xs) for k,a in self.levels.items() 
        }

    def demodulate(self, seq, bins):
        step = len(seq) // bins
        out  = np.empty(bins, dtype=int)
        for i,j in enumerate(range(0, step * bins, step)):
            mpb = np.median(np.abs(seq[j:j+step]))
            k = min(self.levels.keys(), key = lambda k: np.abs(self.levels[k]-mpb))
            out[i] = k

        return out
        
class FSKModulator(Modulator):
    def signal(self, xs):
        freqs = self.levels
        return {
            k: self.A * np.cos(2*np.pi * f * xs) for k,f in self.levels.items()
        }
    
class PSKModulator(Modulator):

    def signal(self, xs):
        return {
            k: self.A * np.cos(2*np.pi * self.freq * xs + off) for k,off in self.levels.items()
        }