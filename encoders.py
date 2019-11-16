
import abc
import numpy as np


class Encoder(abc.ABC):

    @abc.abstractmethod
    def levels(self):
        """
        Returns
        -------
        List(int)
            list of levels for sequences encoded with this encoder
        """

    @abc.abstractmethod
    def encode(self, seq):
        """
        Parameters
        ----------
        seq : numpy.array
            sequence of binary numbers to encode

        Returns
        -------
        numpy.array
            encoded binary sequence
        """
        pass

    @abc.abstractmethod
    def decode(self, seq):
        """
        Parameters
        ----------
        seq : numpy.array
            sequence of binary numbers to decode

        Returns
        -------
        numpy.array
            decoded sequence of binary numbers
        """
        pass


class NRZEncoder(Encoder):
    def levels(self):
        return [-1, 1]

    def encode(self, seq):
        return np.where(seq, np.ones_like(seq), -np.ones_like(seq))

    def decode(self, seq):
        return np.where(seq == 1, np.ones_like(seq), np.zeros_like(seq))


class NRZLEncoder(Encoder):
    def levels(self):
        return [-1, 1]

    def encode(self, seq):
        return np.where(seq, -np.ones_like(seq), np.ones_like(seq))

    def decode(self, seq):
        return np.where(seq == -1, np.ones_like(seq), np.zeros_like(seq))


class NRZIEncoder(Encoder):
    def levels(self):
        return [-1, 1]

    def encode(self, seq):
        out = np.zeros(len(seq) + 1, dtype=int)
        for (i, x) in enumerate(seq):
            out[i+1] = out[i] ^ 1 if x else out[i]

        out = out * 2 - 1
        return out[1:]

    def decode(self, seq):
        seq = (seq + 1) // 2
        seq = np.insert(seq, 0, 0)
        return np.array([x ^ y for x, y in zip(seq, seq[1:])])


class AMIEncoder(Encoder):
    def levels(self):
        return [-1, 0, 1]

    def encode(self, seq):
        tension = 1
        out = np.zeros(len(seq) + 1, dtype=int)
        for (i, x) in enumerate(seq):
            if x == 0:
                out[i] = 0
            else:
                out[i] = tension
                tension = -tension
        return out[1:]

    def decode(self, seq):
        return np.array([0] + [0 if (x == 0) else 1 for x in seq][:-1])


class PseudoternaryEncoder(Encoder):
    def levels(self):
        return [-1, 0, 1]

    def encode(self, seq):
        tension = 1
        out = np.zeros(len(seq) + 1, dtype=int)
        for (i, x) in enumerate(seq):
            if x == 1:
                out[i] = 0
            else:
                out[i] = tension
                tension = -tension
        return out[1:]

    def decode(self, seq):
        return np.array([0] + [1 if (x == 0) else 0 for x in seq][:-1])


class ManchesterEncoder(Encoder):
    def levels(self):
        return [0, 1]

    def encode(self, seq):
        out = np.array([[0, 1] if x else [1, 0] for x in seq]).ravel()
        out = out * 2 - 1
        return out

    def decode(self, seq):
        seq = (seq + 1) // 2
        return np.array([int(seq[i] < seq[i+1]) for i in range(0, len(seq), 2)])


class DifManchesterEncoder(Encoder):
    def levels(self):
        return [0, 1]

    def encode(self, seq):
        n = len(seq)
        out = np.zeros(2 * n, dtype=int)
        for i in range(0, 2 * n, 2):
            out[i] = out[i-1] ^ 1 if seq[i // 2] else out[i-1]
            out[i+1] = out[i] ^ 1
        out = out * 2 - 1
        return out

    def decode(self, seq):
        seq = (seq + 1) // 2
        it = [0] + list(seq)
        return np.array([int(it[i] != it[i+1]) for i in range(0, len(it) - 1, 2)])
