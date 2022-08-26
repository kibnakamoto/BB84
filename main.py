"""
Copyright (C) 2022 Taha Canturk
Date: August, 24, 2022

This is an implementation of the BB84 protocol that operates on classical bits for creating a shared-secret. Therefore, there isn't measuring a photon's polarization, instead Bob randomizes 50% of the encoded key
"""

import quantumrandom

# photon polarazation encoding
# p for plus
p = {
    '0' : 'H',
    '1' : 'V'
}

# photon polarazation encoding
x = {
    '0' : 'A',
    '1' : 'D'
}

# raise error when there is a ValueError with a quantum object
class QuantumValueError(ValueError):
    pass

# generate real random key in base 2 binary
def gen_rand_key(n):
    rand_key = ''
    for i in range(n):
        rand_key+=str(round(quantumrandom.randint(0,1)))
    return rand_key

class Bb84:
    def __init__(self,key, n):
        self.key = key
        self.shared_secret = None
        self.n = n
    
    def encode(self,key=None):
        if key == None:
            key = self.key
        
        encoded = []
        polarazations = []
        self.polarazations = polarazations
        self.encoded = encoded
        
        for bit in key:
            # do a coin flip to figure out whether to choose
            # between x or p for encoding, this has to be done in a
            # quantum system or chances aren't 50%
            coin_flip = bool(round(quantumrandom.randint(0,1)))
            
            # if coin_flip is true, use x, else use p
            if coin_flip:
                encoded.append(x[bit]) # polarazation encoding
                polarazations.append("x")
            else:
                encoded.append(p[bit])
                polarazations.append("+")
        return encoded
    
    def decode(self,key=None):
        if key == None:
            key = self.key
        
        encoded = []
        polarazations = []
        self.polarazations = polarazations
        self.encoded = encoded
        
        for enc in key:
            # do a coin flip to figure out whether to choose
            # between x or p for encoding, this has to be done in a
            # quantum system or chances aren't 50%
            coin_flip = bool(round(quantumrandom.randint(0,1)))
            
            # if coin_flip is true, use x, else use p
            if coin_flip:
                encoded.append(x[enc]) # polarazation decoding
                polarazations.append("x") # non-orthogonal bases
            else:
                encoded.append(p[enc]) 
                polarazations.append("+") # non-orthogonal bases
        return encoded
    
    # Randomly decode it and keep the new shared-key that is non-random
    def get_new_key(self, other):
        # after Bob encodes the key randomly to decode it, he compares 
        # the the non-orthogonal bases (p,x) publicly, if it doesn't
        # match, they get rid of it, the bits they have left are the result
        
        alice_encoded = self.encoded
        bob_encoded = other.encoded
        n = self.n
        
        if len(alice_encoded) != len(bob_encoded):
            raise QuantumValueError("length of encoded keys don\'t match")
        
        shared_secret = []
        self.shared_secret = shared_secret
        other.shared_secret = shared_secret
        
        for i in range(n):
            if (alice_encoded[i] == bob_encoded[i] and
               self.polarazations[i] == other.polarazations[i]):
                shared_secret.append(alice_encoded[i])
        return shared_secret
    
    def out(self, other):
        val1, val2, pol1, pol2 = '','','',''
        for i in range(self.n):
            val1 += self.shared_secret[i] + ' | '
            pol1 += self.polarazations[i] + ' | '
            val2 += other.shared_secret[i] + ' | '
            pol2 += other.polarazations[i] + ' | '
        le = len(val1)
        print(f"{'-'*(le-14)//2}shared secrets{'-'*(le-14)//2}")
        print(f"Alice\'s: {val1}")
        print(f"polar:    {pol1}")
        print('-'*le)
        print(f"Bob\'s: {val2}")
        print(f"polar:  {pol2}")

# n is the length of bits of the shared secrets
n = 2

alice_key = gen_rand_key(n=n)
alice = Bb84(key=alice_key,n=n)
print(alice_key)
# Alice encodes her key
alice.encode()

# Bob decodes Alice's encoded key by re-encoding it, only some of it will be decoded so the shared-secret will be created by keeping the correct bits
bob = Bb84(key=alice.encoded,n=n)
bob.encode()

# alice and Bob generates shared-secrets
alice.get_new_key(other=bob,n=n)
alice.out(other=bob)

# for photon polarization measurement:
# for a 50/50 bit measurement
# let polarizer angle = 38 degrees
# let photon angle = 83 degrees

"""
Data Table for theta of photon
H:  0 = 0
V: 1 = 90
D: 0 = 45
A: 1 = 135
"""
