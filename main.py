"""
Copyright (C) 2022 Taha Canturk
Date: August, 24, 2022

This is an implementation of the BB84 protocol
"""
import numpy as np
import quantumrandom
import qutip as qt

"""
Data Table for theta of photon
p:          qubit states
H:  0 = 0   |0>
V: 1 = 90   |1>
x:
D: 0 = 45   1/sqrt(2) [|0> + |1>]
A: 1 = 135  1/sqrt(2) [|0> - |1>]
"""

# photon polarazation encoding
# p for plus
p = {
    '0': 'H',
    0: 'H',
    '1': 'V',
    1: 'V'
}

p_d = {
    0: 0,
    1: 90
}

# encode classical bits into qubits, this is the data that Alice sends to Bob
encode = {
    '0': qt.basis(2, 0),  # ground state
    '1': qt.basis([2, 1])  # excited state
}

# photon polarazation encoding
x = {
    '0': 'A',
    0: 'A',
    '1': 'D',
    1: 'A'
}

x_d = {
    0: 45,
    1: 135
}

# raise error when there is a ValueError with a quantum object
class QuantumValueError(ValueError):
    pass


# generate real random key in base 2 binary
def gen_rand_key(n):
    rand_key = ''
    for i in range(n):
        rand_key += str(round(quantumrandom.randint(0, 1)))
    return rand_key

# linear polarization of a single photon
def linear_polarization(theta, alpha=np.uint16(0)):
    if alpha == 0:
        exp_a = 1.e+0
    else:
        exp_a = np.exp(alpha)
    _x_ = qt.basis(2, 0)  # ground state
    y = qt.basis(2, 1)  # excited state
    phi_x = np.cos(theta)*exp_a
    phi_y = np.sin(theta)*exp_a
    phi = _x_*phi_x + y*phi_y
    return phi

class Bb84:
    def __init__(self, key, n):
        self.key = key
        self.shared_secret = None
        self.n = n

    # encode classical bits of shared-key to photon qubits
    def encode(self, key=None):
        if key == None:
            key = self.key

        encoded = []
        bases = []
        polarizations = []
        self.polarizations = polarizations
        self.bases = bases
        self.encoded = encoded

        for bit in key:
            # do a coin flip to figure out whether to choose
            # between x or p for encoding, this has to be done in a
            # quantum system or chances aren't 50%
            coin_flip = bool(round(quantumrandom.randint(0, 1)))

            # if coin_flip is true, use x, else use p
            if coin_flip:
                polarizations.append(x[bit])  # polarazation encoding
                bases.append("x")
            else:
                polarizations.append(p[bit])
                bases.append("+")
            encoded.append(encode[bit])
        return encoded

    def decode(self, key=None):
        if key == None:
            key = self.key

        decoded = []
        bases = []
        polarizations = []
        self.polarizations = polarizations
        self.bases = bases
        self.decoded = decoded

        for enc in key:
            # do a coin flip to figure out whether to choose
            # between x or p for encoding, this has to be done in a
            # quantum system for real random
            coin_flip = bool(round(quantumrandom.randint(0, 1)))

            # if coin_flip is true, use x, else use p
            tmp = int(enc[0][0][0].real)
            if coin_flip:
                polarizations.append(x[tmp])  # polarazation decoding
                bases.append("x")  # non-orthogonal bases
                theta = x_d[tmp]
            else:
                polarizations.append(p[tmp])
                bases.append("+")  # non-orthogonal bases
                theta = p_d[tmp]
            phi = linear_polarization(theta)
        return decoded

    def get_new_key(self, other):
        # after Bob encodes the key randomly to decode it, he compares 
        # the non-orthogonal bases (p,x) publicly, if it doesn't
        # match, they get rid of it, the bits they have left are the result

        alice_encoded = self.encoded
        bob_encoded = other.decoded
        n = self.n

        if len(alice_encoded) != len(bob_encoded):
            raise QuantumValueError("length of encoded keys don\'t match")

        shared_secret = []
        self.shared_secret = shared_secret
        other.shared_secret = shared_secret

        for i in range(n):
            if (alice_encoded[i] == bob_encoded[i] and
                    self.bases[i] == other.bases[i]):
                shared_secret.append(alice_encoded[i])
        return shared_secret

    def out(self, other):
        val1, val2, base1, base2, pol1, pol2 = '', '', '', '', '', ''
        for i in range(self.n):
            val1 += self.shared_secret[i] + ' | '
            base1 += self.bases[i] + ' | '
            pol1 += self.polarizations[i] + ' | '
            val2 += other.shared_secret[i] + ' | '
            pol2 += other.polarizations[i] + ' | '
            base2 += other.bases[i] + ' | '
        le = len(val1)
        print(f"{'-' * (le - 14) // 2}shared secrets{'-' * (le - 14) // 2}")
        print(f"Alice\'s: {val1}")
        print(f"base:     {base1}")
        print(f"polar:    {pol1}")
        print('-' * le)
        print(f"Bob\'s:   {val2}")
        print(f"base:     {base2}")
        print(f"polar:    {pol2}")


# n is the length of bits of the shared secrets
n = 2

alice_key = gen_rand_key(n=n)
alice = Bb84(key=alice_key, n=n)
print("alice_key: ",alice_key)

# Alice encodes her key
alice.encode()

# Bob decodes Alice's encoded key by re-encoding it, only some of it will be decoded so the shared-secret will be
# created by keeping the correct bits
bob = Bb84(key=alice.encoded, n=n)
bob.decode()

# alice and Bob generates shared-secrets
alice.get_new_key(other=bob)
alice.out(other=bob)
