#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:46:54 2016

@author: larry
"""
from random import random, choice, shuffle
import numpy as np
import time
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
        return 0
    elif bit == 1:
        return 1
    else:
        return "?"
        

def create_key(number_of_bits=8):
    """
    Creates key to be used in QKD. Key size will be variable. Also logs string to be encrypted
    """    
    string_to_be_encrypted = "supercalifragilisticxpalidocious"
    # Create the key
    possible_bits = [1, 0]
    random_key = [choice(possible_bits) for i in range(number_of_bits)]
    print(random_key)
    number_of_bits = int(number_of_bits)
    return random_key, string_to_be_encrypted, number_of_bits
        
    
    
def apply_quantum_gates(number_of_bits, random_key):
    """
    Applies either Hadamard or identity quantum gate to each bit in number_of_bits.
    """

    # Create Qubits to represent the key
    # Apply Hadamard and identity gates randomly
    alice_gate_list = []
    alice_qbit_list = []
    bob_gate_list = []
    bob_key_recovered = []
    probabilities = []
    possible_gates = ['hadamard', 'identity']
    for i in range(number_of_bits):
        qbit = QKD()
        qbit_value = 0
        gate_chosen = choice(possible_gates)
        
        #applying Hadamard Gate
        if gate_chosen == 'hadamard':
            qbit_value = apply_hadamard_gate(random_key[i], mode = "encoding")
            alice_gate_list.append("{0}H".format(i + 1))
                
        else :
            #applying identity gate
            qbit_value = apply_identity_gate(random_key[i])
            alice_gate_list.append("{0}I".format(i + 1))
            
        probabilities.append((qbit.alpha, qbit.beta))
        alice_qbit_list.append(qbit_value)
        
#        print('gate: {0}; qubit: {1}'.format(gate_chosen, str(qbit)))
        
    alice_gate_tuple_1 = (alice_gate_list)
    
    for i in range(number_of_bits):
        cbit_value = 0
        gate_chosen = choice(possible_gates)
        
        #applying Hadamard Gate
        if gate_chosen == 'hadamard':
            cbit_value = apply_hadamard_gate(alice_qbit_list[i], mode = "decoding")
            bob_gate_list.append("{0}H".format(i + 1))
                
        else :
            #applying identity gate
            cbit_value = apply_identity_gate(alice_qbit_list[i])
            bob_gate_list.append("{0}I".format(i + 1))
            
        bob_key_recovered.append(cbit_value)

    
#        print('gate: {0}'.format(gate_chosen))
    
    gate_matches = [i if i == j else "No Match" for i, j in zip(bob_gate_list, alice_gate_list)]
    return gate_matches, bob_key_recovered, alice_qbit_list, alice_gate_list, bob_gate_list

            
def match_qbits(gate_matches, alice_qbit_list, alice_gate_list, bob_key_recovered, bob_gate_list, random_key, print_gates=True):
    """
    Finds qubits that correspond to gate matches and matches a selection of those qubits.
    """        
    
    if gate_matches == []:
        print("Whoops! The random gate generators did not produce any gates in common!")
        print(gate_matches)
        # using counters bc list indexes start at 0
    else :
        # finds the corresponding qubits to the gate matches
        alice_qbit_nonint_matches = []
        for gate_index, gate_string in enumerate(gate_matches):
            if "H" in gate_string or "I" in gate_string:
                alice_qbit_nonint_matches.append(str(gate_index))
            else:
                continue
            
        # chooses Alice's qubits to be disclosed
        # checks that the choice generated 2 different numbers
        alice_qbit_matches = [int(x) for x in alice_qbit_nonint_matches]
        len_of_qbit_matches = len(alice_qbit_matches)
        sample_number = len_of_qbit_matches / 2
        
        # Chooses qubits here
        # also checks equality
        list_of_chosen_matches = [i for i in range(len_of_qbit_matches)]
        shuffle(list_of_chosen_matches)
        # list_of_chosen_matches = shuffle(list_of_chosen_matches)
        disclosed_qbits = [alice_qbit_matches[list_of_chosen_matches[i]] for i in range(sample_number)]
                    
        #creates lists of actual qubits and matches them
        bob_value_list = [bob_key_recovered[x] for x in disclosed_qbits]
        alice_value_list = [random_key[x] for x in disclosed_qbits]
        qbit_matches = [i for i, j in zip(bob_value_list, alice_value_list) if i == j]
        if len(qbit_matches) < len(bob_value_list):
            raise Exception("Communications error! Security is possibly compromised!")
        else:
            print('Lists match -- Key is secure!!\nKey: {0}'.format(qbit_matches))

    if print_gates == True:
        print(random_key)
        print(alice_gate_list)
        print(bob_gate_list)
        print(gate_matches)
        print(alice_qbit_matches)
        print(disclosed_qbits)
        print('bob list = {0}'.format(bob_value_list))
        print('alice list = {0}'.format(alice_value_list))
        print('matches: {0}'.format(qbit_matches))

    return qbit_matches
"""
EXPERIMENTAL
def eve_interference(alice_qbit_list):
    """"""
    Runs simulated interference from Eve, the third party in BB84
    """"""
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
"""

def aes_encryption(key):
    """
    Applies AES encryption using distributed key
    """
    key_length = len(key)
    if key_length < 16:
        for i in range(16-key_length):
            new_bit = choice([1, 0])
            key.format(new_bit)
            
        

def run_main():

    time1 = time.time()
    random_key, string_to_be_encrypted, number_of_bits = create_key(number_of_bits=32)
    time2 = time.time()
    print("random_key_runtime: {0} seconds.".format(time2 - time1))
    gate_matches, bob_key_recovered, alice_qbit_list, alice_gate_list, bob_gate_list = apply_quantum_gates(number_of_bits, random_key)
    time3 = time.time()
    print("apply_quantum_gates_runtime: {0} seconds.".format(time3 - time2))
    #    alice_qbit_list = eve_interference(alice_qbit_list)
    qbit_matches = match_qbits(gate_matches, alice_qbit_list, alice_gate_list, bob_key_recovered, bob_gate_list, random_key, print_gates=False)
    print("Runtime: {0} seconds.".format(time.time() - time3))
    
# Create the key for Alice
    # Make a random list of quantum gates Alice
    # Apply the gates to each key bit to create the quantum qubit states
    # Send the qubits to Bob
    # Make a random list of quantum gates for Bob
    # Apply the gates to qubits received from Alice
    # Get the set of matching gates between Alice and Bob
    # From the matching gates choose half and the bit values for Alice and Bob
    # If the bit values match, use the remaining bits from matching gates as a key
    # Use the key to Encrypt the data using AES        


if __name__ == '__main__':
    run_main()
    