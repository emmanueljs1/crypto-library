"""
Created on Sun Dec 10 17:49:22 2017

@author: emma & julia
"""

from random import randint
from cryptography.fernet import Fernet


class Encryptor(object):

    def __init__(self):
        ''' an encryptor is initialized with a random seed and tap position '''
        length = randint(15, 30)
        self.seed = []
        for _ in range(length):
            self.seed += [1 if randint(0, 1) == 1 else 0]
        self.tap = randint(0, length)
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    @classmethod
    def encryptor_from_seed_and_tap(cls, seed, tap):
        ''' allows an encryptor to be constructed with a predetermined
            seed and tap position '''
        if tap < 0 or tap > len(seed):
            raise Exception("invalid seed")

        encryptor = Encryptor()
        seed_arr = []

        if len(seed) < 2:
            raise Exception('seed too short')

        for i in range(len(seed)):
            if seed[i] != '1' and seed[i] != '0':
                raise Exception("invalid seed")
            else:
                seed_arr += [int(seed[i])]

        encryptor.seed = seed_arr
        encryptor.tap = tap
        return encryptor

    def pseudorandom_bits(self):
        ''' creates a pseudorandom bit generator (based on LFSR) '''
        seed = self.seed[:]
        while True:
            new_bit = seed[0] ^ seed[self.tap]
            seed = seed[1:] + [new_bit]
            yield new_bit

    def __encode(self, s):
        bin_str = ''

        for byte in bytes(s, 'utf-8'):
            bin_str += format(byte, 'b')

        return bin_str

    def __decode(self, s):
        index = 0
        decoded = ''
        while index < len(s):
            bits = ''
            for _ in range(7):
                if index >= len(s) or (s[index] != '1' and s[index] != '0'):
                    raise Exception("string not a binary encoding")

                bits += s[index]
                index += 1
            decoded += chr(int(bits, 2))

        return decoded

    def decrypt_LFSR(self, s):
        ''' uses the encryptor to decrypt a stirng previously
            encrypted using the encryptor '''
        bits = self.pseudorandom_bits()
        decrypted = ''

        for char in s:
            decrypted += str(int(char) ^ next(bits))

        return self.__decode(decrypted)

    def encrypt_LFSR(self, s):
        ''' uses the encryptor to encrypt the string s
            into a string of 1s and 0s '''
        bits = self.pseudorandom_bits()
        encoded = self.__encode(s)
        encrypted = ''

        for char in encoded:
            encrypted += str(int(char) ^ next(bits))

        return encrypted

    def decrypt(self, s):
        return self.fernet.decrypt(s.encode('utf-8')).decode('utf-8')

    def encrypt(self, s):
        return self.fernet.encrypt(s.encode('utf-8')).decode('utf-8')

    def __str__(self):
        s = self.seed
        k = self.key
        t = self.tap
        return "Encryptor w/ seed {}, tap pos {}, key {}".format(s, t, k)

    def __repr__(self):
        return str(self)

    @classmethod
    def encrypt_with_lfsr(cls, seed, tap, s):
        ''' uses pseudorandom bits generated using LFSR to encrypt s '''
        encryptor = Encryptor.encryptor_from_seed_and_tap(seed, tap)
        return encryptor(s)

if __name__ == '__main__':
    encryptor = Encryptor()
    s = "'hello'"
    print(s, end=" ")
    print("encrypts to '{}'".format(encryptor.encrypt(s)), end=" ")
    print("with cryptography lib and to", end=" ")
    print("'{}' with LFSR".format(encryptor.encrypt_LFSR(s)))
