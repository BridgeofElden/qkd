#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:46:54 2016

@author: larry
"""
from random import random, choice
import numpy as np
        
class Qubit():
    """Creates a quantum bit, the basic unit of quantum computing.
    Has probabilities alpha and beta"""
    
    
    def __init__(self):
        self.alpha = np.sqrt(random())
        self.beta = np.sqrt(1-self.alpha**2)
        self.classic_basis_vector = np.array([self.alpha, self.beta])
        self.hadamard_basis_vector = np.array(
                                [(self.alpha + self.beta)/np.sqrt(2),
                                 (self.alpha - self.beta)/np.sqrt(2)])
        
    def __str__(self):
        output_string = "classic_basis: ket_0: {0}; ket_1: {1}\n" \ 
                        "hadamard_basis: ket_0: {2}; ket_1: {3}"
        return output_string.format(classic_basis_vector[0],
                                    classic_basis_vector[1],
                                    hadamard_basis_vector[0],
                                    hadamard_basis_vector[1])
    
    @staticmethod    
    def tensor_product(qubit_one, qubit_two):
        """
        TO DO: add in FOIL and make into state
        
        Uses tensor products to manipulate bits into quantum state
        """
        if isinstance(qubit_one, Qubit) and isinstance(qubit_two, Qubit):
            return np.outer(qubit_one.classic_basis_vector,
                            qubit_two.classic_basis_vector)
        else:
            raise Exception("Must use two Qubits to determine tensor product")
            
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
        
    def observe_qubit(self):
        pass


def create_key(number_of_bits):
    """
    Creates key to be used in QKD. Key size will be variable. Also logs string to be encrypted
    """    
    string_to_be_encrypted = "If it was easy, everyone would do it!"
    # Create the key
    possible_bits = [1, 0]
    random_key = [choice(possible_bits) for i in range(number_of_bits)]
    return random_key



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
    
    probabilities = []
    possible_gates = ['hadamard', 'identity']
    counter = 0
    for i in range(number_of_bits):
        qbit = Qubit()
        gate_chosen = choice(possible_gates)
        
        #applying Hadamard Gate
        if gate_chosen == 'hadamard':
            qbit.apply_hadamard_gate(random_key[i])
            alice_gate_.append("{0}H".format(counter))
            probabilities.append(qbit)
            probability
                
            else :
                sign = "-"
                alice_qbit_list.append(sign)
                
        else :
            qbit.apply_identity_gate()
            alice_gate_list.append("{0}I".format(counter))
            probabilities.append(qbit)
            number_generator = random()
            
            if number_generator > qbit.ket_1 and number_generator <= 1:
                number = 1                
            else :
                number = 0
                
            qbit_list.append(number)

        
        counter += 1
        print('gate: {0}; qubit: {1}'.format(gate_chosen, qbit))
    
    bob_qbit_list = []
    bob_gate_list = []
    counter = 1
    for i in range(number_of_bits):
        qbit = Qubit()
        selected_bit = alice_measurement_list[i]       
        gate_chosen = choice(possible_gates)
        
        if gate_chosen == "hadamard":
            bob_gate_list.append("{0}H".format(i))
            decoded_qbit = qbit.apply_hadamard_gate(qbit_list.index(i), mode == "decoding")
                
        else :
            bob_gate_list.append("{0}I".format(i)
            decoded_qbit = qbit.apply_identity_gate(qbit_list.index(i))

        bob_qbit_list.append(decoded_qbit)
    list_of_matched_numbers = []
    gate_matches = [i for i, j in zip(bob_gate_list, alice_gate_list) if i == j]
                    
                    
            
def match_qbits(gate_matches)
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
        equality_bool = True
        len_of_qbit_matches = len(alice_qbit_matches)
        sample_number = len_of_qbit_matches/2
        if isinstance(sample_number, int):
            continue
        else :
            sample_number = str(round(sample_number))
        # Chooses qubits here
        # also checks equality
        disclosed_qbits = [choice(alice_qbit_matches) for i in range(sample_number)]
                
        for i in gate_matches:
            position_in_list = counter - 1
            if "{0}".format(counter) in gate_matches.index(position_in_list):
                qbit_nonint_matches.append(gate_matches.index(position_in_list))
            else :
                continue
            counter += 1
            
            
        #creates lists of actual qubits and matches them
        bob_value_list = [bob_qbit_list.index(disclosed_qbits.index(x)) for x in range(len(disclosed_qbits))]
        alice_value_list = [alice]
    
             
    
                
                
    print(alice_gate_list)
    print(bob_gate_list)
    print(gate_matches)
        

def run_main():
    
    # Create the key for Alice
    # Make a random list of quantum gates Alice
    # Apply the gates to each key bit to create the quantum qubit states
    # Send the qubits to Bob
    # Make a random list of quantum gates for Bob
    # Apply the gates to qubits received from Alice
    # Get the set of matching gates between Alice and Bob
    # From the matching gates choose half and the bit values for Alice and Bob
    # If the bit values match, use the remaining bits from matching gates as a key
    # Use the key to AES Encrypt the data
    random_key = create_key(number_of_bits)        


if __name__ == '__main__':
    run_main()
    