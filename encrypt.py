"""
Created on Sun Dec 10 17:49:22 2017

@author: emma & julia
"""

from random import randint
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from Crypto.Cipher import AES


class Encryptor(object):

    def __init__(self):
        ''' an encryptor is initialized with a random seed and tap position '''
        length = randint(15, 30)
        self.seed = []
        seed_str = ''
        for _ in range(length):
            bit = 1 if randint(0, 1) == 1 else 0
            self.seed += [bit]
            seed_str += '{}'.format(bit)
        self.tap = randint(0, length - 1)
        self.key = Fernet.generate_key()
        self.AES_key = ''

        for _ in range(16):
            self.AES_key += str(randint(0, 9))

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

    @classmethod
    def encrypt_with_aes(cls, AES_key, s):
        ''' encrypts using AES with given key '''
        padded_s = s[:]
        padding = len(s) % 16
        for _ in range(16 - padding):
            padded_s += ' '
        cipher = AES.new(AES_key, AES.MODE_CBC, 'This is an IV456')
        return b64encode(cipher.encrypt(padded_s)).decode('utf-8')

    @classmethod
    def decrypt_with_aes(cls, AES_key, s):
        ''' decrypts using AES with given key '''
        cipher = AES.new(AES_key, AES.MODE_CBC, 'This is an IV456')
        return cipher.decrypt(b64decode(s)).decode('utf-8').strip()

    def encrypt_AES(self, s):
        ''' encrypts the string s using encryptor's AES '''
        return Encryptor.encrypt_with_aes(self.AES_key, s)

    def decrypt_AES(self, s):
        ''' decrypts the string s using encryptor's AES '''
        return Encryptor.decrypt_with_aes(self.AES_key, s)

    @classmethod
    def decrypt_with_sac(self, key, s):
        ''' decrypts using symmetric authenticated cryptography
            with given key '''
        fernet = Fernet(key)
        return fernet.decrypt(s.encode('utf-8')).decode('utf-8')

    @classmethod
    def encrypt_with_sac(self, key, s):
        ''' decrypts using symmetric authenticated cryptography
            with given key '''
        fernet = Fernet(key)
        return fernet.encrypt(s.encode('utf-8')).decode('utf-8')

    def decrypt(self, s):
        ''' decrypts using symmetric authenticated cryptography
            with encryptor's key '''
        return Encryptor.decrypt_with_sac(self.key, s)

    def encrypt(self, s):
        ''' encrypts using symmetric authenticated cryptography
            with encryptor's key '''
        return Encryptor.encrypt_with_sac(self.key, s)

    def pseudorandom_bits(self):
        ''' creates a pseudorandom bit generator (based on LFSR) '''
        seed = self.seed[:]
        while True:
            new_bit = seed[0] ^ seed[self.tap]
            seed = seed[1:] + [new_bit]
            yield new_bit

    def __encode(self, s):
        ''' encode a string into binary '''
        bin_str = ''

        for byte in bytes(s, 'utf-8'):
            bin_str += format(byte, 'b')

        return bin_str

    def __decode(self, s):
        ''' decode a string from binary '''
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

    @classmethod
    def encrypt_with_lfsr(cls, seed, tap, s):
        ''' uses pseudorandom bits generated using LFSR to encrypt s '''
        encryptor = Encryptor.encryptor_from_seed_and_tap(seed, tap)
        return encryptor.encrypt_LFSR(s)

    @classmethod
    def decrypt_with_lfsr(cls, seed, tap, s):
        ''' uses pseudorandom bits generated using LFSR to decrypt s '''
        encryptor = Encryptor.encryptor_from_seed_and_tap(seed, tap)
        return encryptor.decrypt_LFSR(s)

    def __str__(self):
        s = self.seed
        k = self.key
        t = self.tap
        q = self.AES_key
        return "seed: {}\ntap: {}\nSAC key: {}\nAES key: {}".format(s, t, k, q)

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    encryptor = Encryptor()
    s = "hey"
    print(s, end=" ")
    SAC_token = encryptor.encrypt(s)
    print("encrypts to '{}'".format(SAC_token), end=" ")
    print("with symmetric authenticated cryptography and to", end=" ")
    LFSR_token = encryptor.encrypt_LFSR(s)
    print("'{}' with LFSR and to".format(LFSR_token), end=" ")
    AES_token = encryptor.encrypt_AES(s)
    print("'{}' with AES using".format(AES_token))
    print(str(encryptor))
