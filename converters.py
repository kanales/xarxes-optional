from encryption import Encryptor
from utils import pipe
import numpy as np


class StringConverter:
    from_int = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    to_int = {c: i for i, c in enumerate(from_int)}
    int_size = 8

    def __init__(self, enc: Encryptor):
        self.enc = enc

    def int2bin(self, itr):
        """
        Parameters
        ----------
        itr : Ierable

        Returns
        -------
        numpy.array
            Array containing the integers in the input encoded as bytes
        """
        return np.array([int(i) for n in itr for i in bin(n)[2:].zfill(8)], dtype=np.int8)

    def bin2int(self, arr):
        """
        Parameters
        ----------
        arr : np.array
            Array containing a sequence of bits

        Returns
        -------
        numpy.array
            Array containing the numbers represented in the input sequence of bits
        """
        ints = []
        for i in range(0, len(arr), self.int_size):
            num = ''.join(str(i) for i in arr[i:i+self.int_size])
            ints.append(int(num, 2))

        return np.array(ints)

    def ascii2int(self, seq):
        return np.array([ord(c) for c in seq])

    def int2ascii(self, seq):
        return ''.join(chr(i) for i in seq)

    def str2int(self, seq):
        """
        Parameters
        ----------
        inp : Ierable
        Returns
        -------
        numpy.array
            Array containing the indices of the encoded characters
        """
        lst = [
            self.to_int[c.lower()] for c in seq if c in self.from_int
        ]
        return np.array(lst)

    def int2str(self, arr):
        """
        Parameters
        ----------
        inp : Ierable

        Returns
        -------
        numpy.array
            Array containing the indices of the encoded characters
        """
        return ''.join(self.from_int[i] for i in arr)

    def from_string(self, seq):
        mask = [c in self.from_int for c in seq]
        seq = list(seq)

        subseq = self.str2int([c for c in seq if c in self.from_int])
        subseq = self.enc.encrypt(subseq)
        subseq = self.int2str(subseq)

        j = 0
        for i, c in enumerate(seq):
            if mask[i]:
                seq[i] = subseq[j]
                j += 1

        seq_int = self.ascii2int(seq)
        return self.int2bin(seq_int)

    def to_string(self, seq):
        seq = self.bin2int(seq)
        seq = self.int2ascii(seq)

        mask = [c in self.from_int for c in seq]

        subseq = self.str2int([c for c in seq if c in self.from_int])
        subseq = self.enc.decrypt(subseq)
        subseq = self.int2str(subseq)

        seq = list(seq)
        j = 0
        for i, c in enumerate(seq):
            if mask[i]:
                seq[i] = subseq[j]
                j += 1

        return ''.join(seq)
