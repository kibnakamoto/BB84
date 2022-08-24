"""
Copyright (C) 2022 Taha Canturk
Date: August, 24, 2022
"""

import quantumrandom

# photon polarazation encoding
# p for plus
p = {
    0 : 'H',
    1 : 'V'
}

# photon polarazation encoding
x = {
    0 : 'A',
    1 : 'D'
}

# raise error when there is a ValueError with a quantum object
class QuantumValueError(ValueError):
    pass

class Bb84:
    def __init__(self,key):
        self.key = key
    
    # generate real random key in base 2 binary
    def gen_rand_key(self,n):
        rand_key = ''
        for i in range(n):
            rand_key+=str(quantumrandom.randint(0,n))
        return rand_key
    
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
            coin_flip = quantumrandom.get_data(data_type='bool',
                                               array_length=1)[0]
            
            # if coin_flip is true, use x, else use p
            if coin_flip:
                pol = x[bit] # polarazation encoding
                encoded.append(pol)
            else:
                pol = p[bit]
                encoded.append(pol)
            polarazations.append(bit)
        return encoded
    
    # Randomly decode it and keep the new shared-key that is non-random
    def get_new_key(self, alice_encoded, bob_encoded=None, n=None):
        # after Bob encodes the key randomly to decode it, he compares 
        # the the non-orthogonal bases (p,x) publicly, if it doesn't
        # match, they get rid of it, the bits they have left are the result
        if bob_encoded == None:
            # since bob encodes last, class member encoded will be Bob's
            # (only if same object is used)
            bob_encoded = self.encoded
        
        if n == None:
            n = len(alice_encoded)
        
        if len(alice_encoded) == len(bob_encoded):
            raise QuantumValueError("length of encoded keys don\'t match")
        
        shared_secret = []
        self.shared_secret = shared_secret
        
        for i in range(n):
            if alice_encoded[i] == bob_encoded[i]:
                shared_secret.append(alice_encoded[i])
        return shared_secret

# n is the length of bits of the shared secrets
n = 2

alice_key = gen_rand_key(n)
