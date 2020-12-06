from rotor_details import Rotors

class Enigma:
    """
    Simulation of Enigma machine used by the Germans during World War 2.
    """
    def __init__(self, plugboard = {" ": " "}, rotors = None, rotor_settings = None):
        self.base_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if type(plugboard) is not dict:
            self.plugboard = {" ": " "}

        self.reflector = Rotors.EnigmaI[2] # gonna change this

        if rotors is None or type(rotors) is not list:
            self.rotors = Rotors.CommericialEnigmaRotors
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
        self.encrypted_text = ""
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

        temp =  self.rotors[0][self.base_alphabet.index(letter)] 

        

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