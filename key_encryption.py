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
# from Crypto.Cipher import AES
        
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
        

def create_key(number_of_bits=8):
    """
    Creates key to be used in QKD. Key size will be variable. Also logs string to be encrypted
    """    
    string_to_be_encrypted = "supercalifragilisticxpalidocious"
#     Create the key
    possible_bits = [1, 0]
    random_key = [choice(possible_bits) for i in range(number_of_bits)]
#    print(random_key)
    number_of_bits = int(number_of_bits)
    return random_key, string_to_be_encrypted, number_of_bits
        
    
    
def apply_quantum_gates_alice(random_key):
    """
    Applies either Hadamard or identity quantum gate to each bit in number_of_bits.
    """

#     Create Qubits to represent the key
#     Apply Hadamard and identity gates randomly
    alice_qbit_list = []
    probabilities = []
    possible_gates = ['hadamard', 'identity']
    for i in (random_key):
        qbit = QKD()
        gate_chosen = choice(possible_gates)
        
        #applying Hadamard Gate
        if gate_chosen == 'hadamard':
            qbit_value = apply_hadamard_gate(i, mode = "encoding")
                
        else :
            #applying identity gate
            qbit_value = apply_identity_gate(random_key[i])
            
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
        
    for i in range(0, 63):
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


        
#       comparing bits to each other
        if alice_success_bit == bob_success_bit:
            continue
            
            
        else:
            raise Exception ('Eavesdropper detected, aborting communications')
            quit
            

    del bob_success_list[0:number_of_iterations]
    new_key = bob_success_list
        
        




    return new_key
"""
EXPERIMENTAL
"""
def eve_interference(alice_qbit_list):
    """
    Runs simulated interference from Eve, the third party in BB84
    """
    for n in range(len(alice_qbit_list)):
        print(alice_qbit_list)
        alice_qbit = alice_qbit_list[n]
        gate_choice = choice(["hadamard", "identity"])
        if gate_choice == "hadamard":
            encoding_choice = choice(["encoding", "decoding"])
            hadamard_results = apply_hadamard_gate(alice_qbit, mode = "encoding")
            if alice_qbit != hadamard_results:
                alice_qbit_list[n] = hadamard_results
            
            else :
                print("Eavesdropping unsuccessful on bit number {0}".format(n + 1))
                
        else :
            apply_identity_gate(alice_qbit)
    print(alice_qbit_list[n])    
    return alice_qbit_list


def aes_encryption(key):
    """
    Applies AES encryption using distributed key
    """
    key_length = len(key)
    if key_length < 16:
        for i in range(16-key_length):
            new_bit = choice([1, 0])
            key.format(new_bit)
            
time_list_1 = []
time_list_2 = []
time_list_3 = [] 

def run_main(time_list_1, time_list_2, time_list_3): 
    time1 = time.time()
    random_key, string_to_be_encrypted, number_of_bits = create_key(number_of_bits=128)
    time2 = time.time()
    print("random_key_runtime: {0} seconds.".format(time2 - time1))
    alice_qbit_list, possible_gates = apply_quantum_gates_alice(random_key)
    bob_bit_list = apply_quantum_gates_bob(alice_qbit_list, possible_gates)
    time3 = time.time()
    print("apply_quantum_gates_runtime: {0} seconds.".format(time3 - time2))
    match_qbits(random_key, bob_bit_list)
    #    alice_qbit_list = eve_interference(alice_qbit_list)
    
    time4 = time.time()
    print("Runtime: {0} seconds.".format(time.time() - time1))
    time_list_1.append(time2 - time1)
    time_list_2.append(time3 - time2)
    time_list_3.append(time4 - time1)
    return time_list_1, time_list_2, time_list_3
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
    run_main(time_list_1, time_list_2, time_list_3)

    
    
    
    

    