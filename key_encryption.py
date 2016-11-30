#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:46:54 2016

@author: larry
"""
from random import random, choice
import numpy as np
from Crypto.Cipher import AES
        
class QKD():
    """
    Creates a quantum bit (qubit), the basic unit of quantum computing.(has probabilities alpha and beta)
    Then, uses the BB84 standard to perform QKD on a random bit string used as the key.
    Includes functions for creating a key, applying quantum logic gates, and matching 
    qubits produced by the quantum logic gates. Also includes message encryption
    Necessary libraries and functions: numpy, random() and choice(), and pycrypto 
    """
    encryption_method = str(raw_input("""
    Which encryption algorithm would you like to use? We have only AES (a symmetric
    encryption method) at the moment.  
    """))
    
    def __init__(self):
        self.alpha = np.sqrt(random())
        self.beta = np.sqrt(1-self.alpha**2)
        self.classic_basis_vector = np.array([self.alpha, self.beta])
        self.hadamard_basis_vector = np.array(
                                [(self.alpha + self.beta)/np.sqrt(2),
                                 (self.alpha - self.beta)/np.sqrt(2)])
        
    def __str__(self, classic_basis_vector, hadamard_basis_vector):
        output_string = """classic_basis: ket_0: {0}; ket_1: {1}\n"  
                        hadamard_basis: ket_0: {2}; ket_1: {3}"""
        return output_string.format(classic_basis_vector[0],
                                    classic_basis_vector[1],
                                    hadamard_basis_vector[0],
                                    hadamard_basis_vector[1])

            
    def apply_hadamard_gate(self, bit, mode="encoding"):
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
            
    def apply_identity_gate(self, bit):
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
        

    def create_key(number_of_bits):
        """
        Creates key to be used in QKD. Key size will be variable. Also logs string to be encrypted
        """    
        string_to_be_encrypted = str(raw_input("What string would you like to encrypt?  "))
        # Create the key
        possible_bits = [1, 0]
        random_key = [choice(possible_bits) for i in range(number_of_bits)]
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
        bob_qbit_list = []
        qbit = QKD()
        probabilities = []
        possible_gates = ['hadamard', 'identity']
        counter = 0
        for i in range(number_of_bits):
            gate_chosen = choice(possible_gates)
            
            #applying Hadamard Gate
            if gate_chosen == 'hadamard':
                qbit_value = qbit.apply_hadamard_gate(random_key[i], mode = "encoding")
                alice_gate_list.append("{0}H".format(counter))
                probabilities.append(qbit)
                    
                    
            else :
                #applying identity gate
                qbit.apply_identity_gate()
                alice_gate_list.append("{0}I".format(counter))
                probabilities.append(qbit)
                
                    
            alice_qbit_list.append(qbit_value)
    
            
            counter += 1
            print('gate: {0}; qubit: {1}'.format(gate_chosen, qbit))
        
        bob_qbit_list = []
        bob_gate_list = []
        counter = 1
        for i in range(number_of_bits):
            gate_chosen = choice(possible_gates)
            
            if gate_chosen == "hadamard":
                bob_gate_list.append("{0}H".format(i))
                decoded_qbit = qbit.apply_hadamard_gate(alice_qbit_list.index(i), mode = "decoding")
                    
            else :
                bob_gate_list.append("{0}I".format(i))
                decoded_qbit = qbit.apply_identity_gate(alice_qbit_list.index(i))
    
            bob_qbit_list.append(decoded_qbit)
        gate_matches = [i for i, j in zip(bob_gate_list, alice_gate_list) if i == j]
        return gate_matches, bob_qbit_list, alice_qbit_list, alice_gate_list, bob_gate_list
                        
                        
                
    def match_qbits(gate_matches, alice_qbit_list, bob_qbit_list, alice_gate_list, bob_gate_list, print_gates = True):
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
            counter = 1
            for i in gate_matches:
                position_in_list = counter - 1
                if "{0}".format(counter) in gate_matches.index(position_in_list):
                    alice_qbit_nonint_matches.append(gate_matches.index(position_in_list))
                else :
                    continue
                counter += 1
            # chooses Alice's qubits to be disclosed
            # checks that the choice generated 2 different numbers
            alice_qbit_matches = [int(x) for x in alice_qbit_nonint_matches]
            len_of_qbit_matches = len(alice_qbit_matches)
            sample_number = len_of_qbit_matches/2
            if isinstance(sample_number, int):
                pass
            else :
                sample_number = str(round(sample_number))
            # Chooses qubits here
            # also checks equality
            disclosed_qbits = [choice(alice_qbit_matches) for i in range(sample_number)]
                    
            for i in gate_matches:
                position_in_list = counter - 1
                if "{0}".format(counter) in gate_matches.index(position_in_list):
                    alice_qbit_nonint_matches.append(gate_matches.index(position_in_list))
                else :
                    continue
                counter += 1
                
                
            #creates lists of actual qubits and matches them
            bob_value_list = [bob_qbit_list.index(disclosed_qbits.index(x)) for x in range(len(disclosed_qbits))]
            alice_value_list = [alice_qbit_list.index(disclosed_qbits.index(x)) for x in range(len(disclosed_qbits))]
            qbit_matches = [i for i, j in zip(bob_value_list, alice_value_list) if i == j]
            if len(qbit_matches) < len(bob_value_list):
                raise Exception("Communications error! Security is possibly compromised!")
            else :
                pass
                
        
                    
        if print_gates == True:           
            print(alice_gate_list)
            print(bob_gate_list)
            print(gate_matches)
            
        else :
            pass
        
        return qbit_matches
        
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
    qbit = QKD()
    
    random_key, string_to_be_encrypted, number_of_bits = qbit.create_key(8)
    qbit.apply_quantum_gates(random_key, number_of_bits)
    qbit.match_qbits(qbit.apply_quantum_gates(number_of_bits, random_key))
    
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
    