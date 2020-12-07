from rotor_details import Rotors

class Enigma:
    """
    Simulation of Enigma machine used by the Germans during World War 2.
    """
    def __init__(self, plugboard = {" ": " "}, rotors = None, rotor_settings = None):
        self.base_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if type(plugboard) is not dict:
            self.plugboard = {" ": " "}
        else:
            self.plugboard = plugboard

        self.reflector = Rotors.EnigmaI[2] # gonna change this

        if rotors is None or type(rotors) is not list:
            self.rotors = [list(rotor) for rotor in Rotors.CommericialEnigmaRotors]
        else:
            self.rotors = rotors
        
        if rotor_settings is None or type(rotor_settings) is not list:
            self.rotor_settings = [0 for i in range(len(self.rotors))]
        else:
            self.rotor_settings = rotor_settings

            if bool(self.rotor_settings) and all(isinstance(elem, str) for elem in self.rotor_settings):
                temp = []

                for index in range(len(self.rotor_settings)):
                    temp.append(self.rotors[index].index(self.rotor_settings[index]))
                
                self.rotor_settings = temp
            else:
                raise ValueError("Rotor settings should be letters.")

        if len(self.rotors) != len(self.rotor_settings):
            raise ValueError("Number of rotor settings should be equal to the number of rotors.")
        
        self.rotor_pointers = self.rotor_settings

        print(self.rotor_pointers)
    
    @property
    def settings(self):
        ret = []

        for index in range(len(self.rotor_settings)):
            ret.append(self.rotors[index][self.rotor_settings[index]])
        
        return ret

    def inbound_rotor(self, letter):
        """
        Inbound input rotor function from right to left.

        Note: di pa dynamic. 
        Base case: 3 rotors
        """
        entry = letter 
        
        out = None

        # First Rotor Logic
        for _ in range(self.rotor_pointers[0]):
            self.rotors[0].insert(0, self.rotors[0][-1])
            self.rotors[0].pop(-1)

        temp = self.rotors[0][self.base_alphabet.index(letter)]
        print(f"ROT1: before: {letter} | after: {temp}")

        #Turn rotor 1
        self.rotor_pointers[0] += 1

        # Second Rotor Logic

        for _ in range(self.rotor_pointers[1]):
            self.rotors[1].insert(0, self.rotors[1][-1])
            self.rotors[1].pop(-1)
        
        before = temp # debug
        temp = self.rotors[1][self.base_alphabet.index(temp)]
        
        print(f"ROT2: before: {before} | after: {temp}\n")

        #Third Rotor Logic 
        for _ in range(self.rotor_pointers[2]):
            self.rotors[2].insert(0, self.rotors[1][-1])
            self.rotors[2].pop(-1)
        
        temp = self.rotors[2][self.base_alphabet.index(temp)]

        # Turn rotor 2 if rotor 1 got a full revolution
        if self.rotor_pointers[0] % 26 == 0:
            self.rotor_pointers[1] += 1
            self.rotor_pointers[0] = 0
        
        # Turn rotor 3 if rotor 2 got full revolution and rotor 1 does not revolve fully
        if self.rotor_pointers[0] % 26 == 0 and self.rotor_pointers[0] % 26 != 0 and self.rotor_pointers[1] >= 25:
            self.rotor_pointers[2] += 1
            self.rotor_pointers[1] = 1

        return temp

    def outbound_rotor(self):
        """
        Outbound input rotor function from left to right.
        """
        pass

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
        pass

    def encrypt_text(self, text: str):
        text = text.upper().replace(" ", "")

        encrypted_text = ""

        for letter in text:
            temp = self.plugboard_operation(letter)

            temp = self.inbound_rotor(temp)

            encrypted_text += temp
        
        return encrypted_text