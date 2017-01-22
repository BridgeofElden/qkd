#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:46:54 2016

@author: larry
"""
from random import random, choice
import numpy as np
import time
from math import ceil
from Crypto.Cipher import AES
        
class QKD():
    """
    Creates a quantum bit (qubit), the basic unit of quantum computing.(has probabilities alpha and beta)
    Then, uses the BB84 standard to perform QKD on a random bit string used as the key.
    Includes functions for creating a key, applying quantum logic gates, and matching 
    qubits produced by the quantum logic gates. Also includes message encryption
    Necessary libraries and functions: numpy, random() and choice(), and pycrypto 
    """
    encryption_method = "AES"
    
    def __init__(self):
        self.alpha = np.sqrt(random())
        self.beta = np.sqrt(1-self.alpha**2)
        self.classic_basis_vector = np.array([self.alpha, self.beta])
        self.hadamard_basis_vector = np.array(
                                [(self.alpha + self.beta)/np.sqrt(2),
                                 (self.alpha - self.beta)/np.sqrt(2)])
        
    def __str__(self):
        output_string = """classic_basis: ket_0: {0}; ket_1: {1}\n"  
                        hadamard_basis: ket_0: {2}; ket_1: {3}"""
        return output_string.format(self.classic_basis_vector[0],
                                    self.classic_basis_vector[1],
                                    self.hadamard_basis_vector[0],
                                    self.hadamard_basis_vector[1])

            
def apply_hadamard_gate(bit, mode="encoding"):
    """
    Apply Hadamard quantum gate to a qbit or a classic bit.
    """
    if mode == "encoding":
        if bit == 0:
            return "+"
        elif bit == 1:
            return "-"
        else:
            return "?"
    elif mode == "decoding":
        if bit == "+":
            return 0
        elif bit == "-":
            return 1
        else:
            return "?"
        
def apply_identity_gate(bit):
    """
    Keeps qbit and classic bit results. Does not not have a mode because
    encoding and decoding methods are the same
    """
    if bit == 0:
        pass
#        return 0
    elif bit == 1:
        pass
#        return 1
    else:
        return "?"
        

def create_key(number_of_bits=128, rerun = False):
    """
    Creates key to be used in QKD. Key size will be variable. Also logs string to be encrypted
    """    
    message = "believe in hope."
#     Create the key
    possible_bits = [1, 0]
    random_key = [choice(possible_bits) for i in range(number_of_bits)]
#    print(random_key)
    number_of_bits = int(number_of_bits)
    if rerun:
        random_key_2 = random_key
        return random_key_2, number_of_bits, message
    else :
        return random_key, number_of_bits, message
    
    
def apply_quantum_gates_alice(random_key):
    """
    Applies either Hadamard or identity quantum gate to each bit in number_of_bits.
    """

#     Create Qubits to represent the key
#     Apply Hadamard and identity gates randomly
    alice_qbit_list = []
    probabilities = []
    possible_gates = ['hadamard', 'identity']
    print(random_key)
    for x in range(len(random_key)):
        qbit = QKD()
        gate_chosen = choice(possible_gates)
        
        #applying Hadamard Gate
        if gate_chosen == 'hadamard':
            qbit_value = apply_hadamard_gate(random_key[x], mode = "encoding")
                
        else :
            #applying identity gate
            qbit_value = apply_identity_gate(random_key[x])
            
        probabilities.append((qbit.alpha, qbit.beta))
        alice_qbit_list.append(qbit_value)
        
        
    return alice_qbit_list, possible_gates
        
def apply_quantum_gates_bob(alice_qbit_list, possible_gates):
    
    bob_bit_list = []    
    for i in (alice_qbit_list):
        gate_chosen = choice(possible_gates)
        
        
#        applying Hadamard Gate
        if gate_chosen == 'hadamard':
            bit_value = apply_hadamard_gate(i, mode = "decoding")
                
        else :
#            applying identity gate
            bit_value = apply_identity_gate(i)
        
        bob_bit_list.append(bit_value)
                            
        
    return bob_bit_list
            


            
def match_qbits(random_key, bob_bit_list):
    """
    Matches lists of bits. Taken from original list and bob's decoded list.
    """
#   choosing bits to compare
    new_key = []
    alice_success_list = []
    bob_success_list = []            
        
    for i in range(len(random_key)):
        alice_bit = random_key[i]
        bob_bit = bob_bit_list[i]
        if bob_bit == "?":
            continue
        else:
#            making lists of successful gate matches
            alice_success_list.append(alice_bit)
            bob_success_list.append(bob_bit)
            
#   determining number of needed iterations for comparing bits             
    bob_success_list_len = len(bob_success_list)
    number_of_iterations = int(ceil(bob_success_list_len/2))
        
    for i in range(0, number_of_iterations):
        alice_success_bit = alice_success_list[i]
        bob_success_bit = bob_success_list[i]


#        print(alice_success_bit)
#        print(bob_success_bit)    
#       comparing bits to each other
        if alice_success_bit == bob_success_bit:
            continue
            
            
        else:
            raise Exception ('Eavesdropper detected, aborting communications')
            quit
            

    del bob_success_list[0:number_of_iterations]
    new_key = bob_success_list
        
        

    print(new_key)


    return new_key
"""
EXPERIMENTAL
"""
def eve_interference(alice_qbit_list):
    """
    Runs simulated interference from Eve, the third party in BB84
    """
    eve_qbit_list = []
    for i in alice_qbit_list:
        gate_choice = choice(["identity", "hadamard"])
        if gate_choice == "identity":
            apply_identity_gate(i)
            eve_qbit_list.append(i)
        else :
            encoding_choice = choice(["encoding", "decoding"])
            new_item = apply_hadamard_gate(i, mode = encoding_choice)
            eve_qbit_list.append(new_item)
    alice_list2 = alice_qbit_list        
    for i in range(len(alice_list2)):
          alice_qbit_list[i] = eve_qbit_list[i]


    
    return alice_qbit_list


def aes_encryption(new_key, message, number_of_bits):
    """
    Applies AES encryption using distributed key
    """
    print(new_key)
    key_length = len(new_key)
    if key_length < 16:
        while key_length < 16:
            random_key_2, number_of_bits, message = create_key(number_of_bits=128, rerun = True)
            alice_qbit_list, possible_gates = apply_quantum_gates_alice(random_key_2)
            bob_bit_list = apply_quantum_gates_bob(alice_qbit_list, possible_gates)
            match_qbits(random_key_2, bob_bit_list)
            for i in range(16-key_length):
                new_bit = choice(random_key_2)
    #            print(random_key)
    #            print("random")
    #            print(new_bit)
    #            print(type(new_bit))
                new_key.append(new_bit)
            key_length = len(new_key)
        IV = "This is an IV123"
        print(new_key)
        key = [str(item) for item in new_key]
        print(key)
        stringified_key = "".join(key)
        object1 = AES.new(stringified_key, AES.MODE_CBC, IV)
        encrypted_text = object1.encrypt(message)
        print(encrypted_text)
        return stringfied_key, encrypted_text
    
    elif key_length > 16:
        number_of_removed_bits = key_length - 16
        second_new_key = new_key[:-(number_of_removed_bits)]
        IV = "This is an IV123"
        print(second_new_key)
        key = [str(item) for item in second_new_key]
        print(key)
        stringified_key = "".join(key)
        object1 = AES.new(stringified_key, AES.MODE_CBC, IV)
        encrypted_text = object1.encrypt(message)
        print(encrypted_text)
        return stringified_key, encrypted_text
    else :
        IV = "This is an IV123"
        print(new_key)
        key = [str(item) for item in new_key]
        print(key)
        stringified_key = "".join(key)
        object1 = AES.new(stringified_key, AES.MODE_CBC, IV)
        encrypted_text = object1.encrypt(message)
        print(encrypted_text)
        return stringified_key, encrypted_text
    
        

    
def aes_decryption(encrypted_text, stringified_key):
    """
    Applies AES decryption using key
    """        
    object2 = AES.new(stringfied_key, AES.MODE_CBC, "This is an IV123")
    decrypted_text = object2.decrypt(encrypted_text)
    print(decrypted_text)
    print(decrypted_text)


    return decrypted_text 

    
    

time_list_1 = []
time_list_2 = []
time_list_3 = []
def run_main(time_list_1, time_list_2, time_list_3, eve = True): 
    time1 = time.time()
    random_key, number_of_bits, message = create_key(number_of_bits=128)
    
    
    time2 = time.time()
    
    print("random_key_runtime: {0} seconds.".format(time2 - time1))
    
    
    alice_qbit_list, possible_gates = apply_quantum_gates_alice(random_key)
    
    
    
    time3 = time.time()
    
    print("apply_quantum_gates_runtime: {0} seconds.".format(time3 - time2))
    if eve:
        alice_qbit_list = eve_interference(alice_qbit_list)
        
    bob_bit_list = apply_quantum_gates_bob(alice_qbit_list, possible_gates)
    new_key = match_qbits(random_key, bob_bit_list)

    
    time4 = time.time()
    
    print("Runtime: {0} seconds.".format(time.time() - time1))
    
    
    time_list_1.append(time2 - time1)
    time_list_2.append(time3 - time2)
    time_list_3.append(time4 - time1)
    return new_key, message, number_of_bits
    """
    Alice makes 128 bit string
    Alice encodes into qubits
    Alice transmits qubits to Bob
    Bob receives qubits
    Bob decodes qubits
    Compare bit strings
    If equal, secure communication
    Use remaining undisclosed qubits as key
    If unequal, unsecure communication (abort)
    
    Alice makes 128 bit string
    Alice encodes into qubits
    Alice transmits qubits to Bob
    Eve receives qubits
    Eve decodes qubits
    Eve reencodes qubits
    Eve transmits to Bob
    Bob receives qubits
    Bob decodes qubits
    Compare bit strings
    If equal, secure communication
    Use remaining undisclosed qubits as key
    If unequal, unsecure communication (abort)
    """      


if __name__ == '__main__':
    new_key, message, number_of_bits = run_main(time_list_1, time_list_2, time_list_3, eve = False)
    print(time_list_1, time_list_2, time_list_3)
    stringfied_key, encrypted_text = aes_encryption(new_key, message, number_of_bits)
    aes_decryption(encrypted_text, stringfied_key)
    
    
    
    

    