import numpy as np
from rotor_details import Rotors
from vigenere import Vigenere
from cryptogram import Crypto, match
from matrix_cryptography import Matrix

class Enigma:
    """
    A modified Enigma machine incorporating different cryptography algorithms.
    """
    def __init__(self, plugboard = {" ": " "}, rotors = None, rotor_settings = None):
        self.base_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if type(plugboard) is not dict:
            self.plugboard = {" ": " "}
        else:
            self.plugboard = plugboard

        self.reflector = 'EJMZALYXVBWFCRQUONTSPIKHGD'

        if rotors is None or type(rotors) is not list:
            self.rotors = [list(rotor) for rotor in Rotors.CommericialEnigmaRotors]
        else:
            self.rotors = rotors
        
        if rotor_settings is None or type(rotor_settings) is not list:
            self.rotor_settings = [0 for i in range(3)]
            self.vigenere = ['A', 'A', 'A', 'A', 'A', 'A']
            self.matrix_crypt = Crypto(np.array([[1, 2, 0], [-1,1,3], [1,-1,-4]]))
        else:
            self.rotor_settings = rotor_settings[0:3]
            self.vigenere = rotor_settings[3:9]
            self.matrix_crypt = [
                [self.base_alphabet.index(i) for i in rotor_settings[9:12]],
                [self.base_alphabet.index(i) for i in rotor_settings[12:15]],
                [self.base_alphabet.index(i) for i in rotor_settings[15:18]]
            ]

            if bool(self.rotor_settings) and all(isinstance(elem, str) for elem in self.rotor_settings):
                temp = []

                for index in range(len(self.rotor_settings)):
                    temp.append(self.rotors[index].index(self.rotor_settings[index]))
                
                self.rotor_settings = temp
            else:
                raise ValueError("Rotor settings should be letters.")

        if len(self.rotors) != len(self.rotor_settings[0:3]):
            raise ValueError("Number of rotor settings should be equal to the number of rotors.")
        
        self.rotor_pointers = self.rotor_settings
        self.vig = Vigenere([self.base_alphabet.index(i) for i in self.vigenere])
    
    @property
    def settings(self):
        ret = []

        for index in range(len(self.rotor_settings)):
            ret.append(self.rotors[index][self.rotor_settings[index]])
        
        return ret
    
    @property 
    def rotor_pointer_settings(self):
        ret = []

        for index in range(len(self.rotor_settings)):
            ret.append(self.rotors[index][self.rotor_pointers[index]])
        
        return ret
    
    def set_plugboard_wiring(self, wirings):
        if type(wirings) is not dict:
            self.plugboard = {" ": " "}
        else:
            self.plugboard = wirings
    
    def set_rotor_settings(self, new_settings):
        if new_settings is None or type(new_settings) is not list:
            self.rotor_settings = [0 for i in range(len(self.rotors))]
        else:
            self.rotor_settings = new_settings[0:3]

            try:
                if bool(self.rotor_settings) and all(isinstance(elem, str) for elem in self.rotor_settings):
                    temp = []

                    for index in range(len(self.rotor_settings)):
                        temp.append(self.rotors[index].index(self.rotor_settings[index]))
                    
                    self.rotor_settings = temp
                else:
                    raise ValueError("Rotor settings should be letters.")
            except ValueError:
                print("Wrong key format, try again.")
                return
        
        self.rotor_pointers = self.rotor_settings
        self.vigenere = new_settings[3:9]
        self.matrix_crypt = [
                [self.base_alphabet.index(i) for i in new_settings[9:12]],
                [self.base_alphabet.index(i) for i in new_settings[12:15]],
                [self.base_alphabet.index(i) for i in new_settings[15:18]]
            ]
    
    def inbound_rotor_map(self, rotor_setting):
        shift = list(self.base_alphabet)

        for _ in range(rotor_setting):
            shift.insert(0, shift[-1])
            shift.pop(-1)
        
        return shift
    
    def outbound_rotor_map(self, rotor_setting):
        shift = list(self.base_alphabet)

        for _ in range(rotor_setting):
            shift.append(shift[0])
            shift.pop(0)
        
        return shift

    def inbound_rotor(self, letter):
        """
        Inbound input rotor function from right to left.

        Note: di pa dynamic. 
        Base case: 3 rotors
        """
        # First Rotor Logic
        temp = self.inbound_rotor_map(self.rotor_pointers[0])[self.base_alphabet.index(letter)]

        # Second Rotor Logic
        temp = self.inbound_rotor_map(self.rotor_pointers[1])[self.base_alphabet.index(temp)]

        #Third Rotor Logic 
        temp = self.inbound_rotor_map(self.rotor_pointers[2])[self.base_alphabet.index(temp)]

        return temp

    def outbound_rotor(self, letter):
        """
        Outbound input rotor function from left to right.
        """
        # Third Rotor
        temp = self.outbound_rotor_map(self.rotor_pointers[2])[self.base_alphabet.index(letter)]

        # Second Rotor 
        temp = self.outbound_rotor_map(self.rotor_pointers[1])[self.base_alphabet.index(temp)]

        # First Rotor 
        temp = self.outbound_rotor_map(self.rotor_pointers[0])[self.base_alphabet.index(temp)]

        return temp
    
    def turn_rotors(self):
        #Turn rotor 1
        self.rotor_pointers[0] += 1
        
        # Turn rotor 2 if rotor 1 got a full revolution
        if self.rotor_pointers[0] % 26 == 0:
            self.rotor_pointers[1] += 1
            self.rotor_pointers[0] = 0
        
        # Turn rotor 3 if rotor 2 got full revolution and rotor 1 does not revolve fully
        if self.rotor_pointers[1] % 26 == 0 and self.rotor_pointers[0] % 26 != 0 and self.rotor_pointers[1] >= 25:
            self.rotor_pointers[2] += 1
            self.rotor_pointers[1] = 1

    def plugboard_operation(self, letter):
        """
        Plugboard that swaps two letters.
        """
        if letter in self.plugboard:
            return self.plugboard[letter]
        else:
            return letter

    def reflector_operation(self, letter):
        """
        Reflects the letters to its own mapping.
        """
        return self.reflector[self.base_alphabet.index(letter)]

    def encrypt_text(self, text: str):
        text = text.upper().replace(" ", "")

        encrypted_text = ""

        for letter in text:
            temp = self.plugboard_operation(letter)

            temp = self.inbound_rotor(letter)

            temp = self.reflector_operation(temp)

            temp = self.outbound_rotor(temp)

            self.turn_rotors()

            temp = self.plugboard_operation(temp)

            encrypted_text += temp
        
        encrypted_text = self.vig.encrypt(encrypted_text)

        processed = Crypto.convert(encrypted_text)

        encrypted_text = Crypto.encode(processed, Matrix(self.matrix_crypt))

        to_text = ""

        for code_group in encrypted_text:
            for code in code_group:
                to_text += f"{code} "
        
        return to_text
    
    def decrypt_text(self, text):
        text = [int(x) for x in text.split(' ')]

        processed = [text[i:i+3] for i in range(0,len(text),3)]

        if len(processed[len(processed)-1]) == 2:
            processed[len(processed)-1].append(0)
        elif len(processed[len(processed)-1]) == 1:
            processed[len(processed)-1].append(0)
            processed[len(processed)-1].append(0)
        
        decoder = Matrix(self.matrix_crypt)

        decoded = Crypto.decode(processed, decoder)

        decoded_message = ""

        for code_group in decoded:
            for code in code_group:
                decoded_message += f"{int(code)} "
        
        decoded_message = decoded_message[0:len(decoded_message)-1]

        message = [int(x) for x in decoded_message.split(' ')]

        converted = ""

        for number in message:
            for key,value in match.items():
                if value == number:
                    converted += key
        
        text = converted.upper().replace(" ", "")

        text = self.vig.decrypt(text)

        decrypted_text = ""

        for letter in text:
            temp = self.plugboard_operation(letter)

            temp = self.inbound_rotor(letter)

            temp = self.reflector_operation(temp)

            temp = self.outbound_rotor(temp)

            self.turn_rotors()

            temp = self.plugboard_operation(temp)

            decrypted_text += temp
        
        return decrypted_text