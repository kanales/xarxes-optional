import numpy as np


class Encryptor:
    _M = np.array([
        [6, 24, 1],
        [13, 16, 10],
        [20, 17, 15]
    ])
    _M1 = np.array([
        [8, 5, 10],
        [21, 8, 21],
        [21, 12, 8],
    ])

    def __init__(self, encmat=None, decmat=None, mod=26):
        self.e = encmat or self._M
        self.d = decmat or self._M1
        self.m = mod
        self.dim = self.e.shape[0]
        assert(np.array_equal(np.eye(self.dim), (self.e @ self.d) % mod))

    def encrypt(self, seq):
        """
        Encrypts sequence of integers, padding to the nearest multiple of 
        `dim` if necessary.

        Parameters
        ----------
        seq : numpy.array
            vector of size `n * dim` with n a natural number
        Returns
        -------
        numpy.array
        vector of size `n * dim`
        """
        n = len(seq)
        pad_length = (self.dim - n % self.dim) % self.dim
        seq = np.pad(seq, (0, pad_length), 'constant')
        seq = seq.reshape([-1, self.dim]).T
        seq = self.e @ seq % 26
        seq = seq.T.ravel()
        return seq

    def decrypt(self, seq):
        """
        Decrypts sequence of integers, padding to the nearest multiple of 
        `dim` if necessary.

        Parameters
        ----------
        seq : numpy.array
            vector of size `n * dim` with n a natural number
        Returns
        -------
        numpy.array
            vector of size `n * dim`
        """
        n = len(seq)
        pad_length = (self.dim - n % self.dim) % self.dim
        seq = np.pad(seq, (0, pad_length))
        seq = seq.reshape([-1, self.dim]).T
        seq = self.d @ seq % 26
        seq = seq.T.ravel()
        return seq[:n]
