import numpy as np

class BinaryConverter:
    def __init__(self, int_size = 8):
        self.int_size = int_size
    
    def encode(self, itr):
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

    def decode(self, arr):
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
        for i in range(0,len(arr), self.int_size):
            num = ''.join(str(i) for i in arr[i:i+self.int_size])
            ints.append(int(num, 2))
            
        return np.array(ints)

class StringConverter:
    # llista_a 
    from_int = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p', 'q','r','s','t','u','v','w','x','y','z']
    to_int = { c:i for i,c in enumerate(from_int)}
    
    
    def decode(self, seq):
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

    def encode(self, arr):
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
