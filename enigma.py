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

        #print(f"init setting: {self.rotor_pointers}")
        #print(f"plugboard: {self.plugboard}")
    
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
            self.rotor_settings = new_settings

            if bool(self.rotor_settings) and all(isinstance(elem, str) for elem in self.rotor_settings):
                temp = []

                for index in range(len(self.rotor_settings)):
                    temp.append(self.rotors[index].index(self.rotor_settings[index]))
                
                self.rotor_settings = temp
            else:
                raise ValueError("Rotor settings should be letters.")
        
        self.rotor_pointers = self.rotor_settings
    
    def inbound_rotor_map(self, rotor_setting):
        shift = list(self.base_alphabet)

        for _ in range(rotor_setting):
            shift.insert(0, shift[-1])
            shift.pop(-1)
        
        #print(' '.join([c for c in self.base_alphabet]))
        #print(' '.join([c for c in shift]))
        return shift
    
    def outbound_rotor_map(self, rotor_setting):
        shift = list(self.base_alphabet)

        for _ in range(rotor_setting):
            shift.append(shift[0])
            shift.pop(0)
        
        #print(' '.join([c for c in self.base_alphabet]))
        #print(' '.join([c for c in shift]))
        return shift

    def inbound_rotor(self, letter):
        """
        Inbound input rotor function from right to left.

        Note: di pa dynamic. 
        Base case: 3 rotors
        """
        # First Rotor Logic
        temp = self.inbound_rotor_map(self.rotor_pointers[0])[self.base_alphabet.index(letter)]
        #print(f"ROT1: before: {letter} | after: {temp}")

        # Second Rotor Logic
        before = temp # debug
        temp = self.inbound_rotor_map(self.rotor_pointers[1])[self.base_alphabet.index(temp)]
        
        #print(f"ROT2: before: {before} | after: {temp}")

        #Third Rotor Logic 
        before = temp
        temp = self.inbound_rotor_map(self.rotor_pointers[2])[self.base_alphabet.index(temp)]
        #print(f"ROT3: before: {before} | after: {temp}")

        return temp

    def outbound_rotor(self, letter):
        """
        Outbound input rotor function from left to right.
        """
        # Third Rotor
        temp = self.outbound_rotor_map(self.rotor_pointers[2])[self.base_alphabet.index(letter)]
        #print(f"ROT1: before: {letter} | after: {temp}")
        # Second Rotor 
        before = temp
        temp = self.outbound_rotor_map(self.rotor_pointers[1])[self.base_alphabet.index(temp)]
        #print(f"ROT2: before: {before} | after: {temp}")
        # First Rotor 
        before = temp
        temp = self.outbound_rotor_map(self.rotor_pointers[0])[self.base_alphabet.index(temp)]
        #print(f"ROT1: before: {before} | after: {temp}")
        return temp
    
    def turn_rotors(self):
        #Turn rotor 1
        self.rotor_pointers[0] += 1
        
        # Turn rotor 2 if rotor 1 got a full revolution
        if self.rotor_pointers[0] % 26 == 0:
            self.rotor_pointers[1] += 1
            self.rotor_pointers[0] = 0
        
        # Turn rotor 3 if rotor 2 got full revolution and rotor 1 does not revolve fully
        if self.rotor_pointers[0] % 26 == 0 and self.rotor_pointers[0] % 26 != 0 and self.rotor_pointers[1] >= 25:
            self.rotor_pointers[2] += 1
            self.rotor_pointers[1] = 1

    def plugboard_operation(self, letter):
        """
        Plugboard that swaps two letters.
        """
        if letter in self.plugboard:
            #print(f"PLUG: before: {letter} | after: {self.plugboard[letter]}")
            return self.plugboard[letter]
        else:
            #print(f"PLUG: before: {letter} | after: {letter}")
            return letter

    def reflector_operation(self, letter):
        """
        Reflects the letters to its own mapping.
        """
        #print(f"REFLECTOR: before: {letter} | after: {self.reflector[self.base_alphabet.index(letter)]}")
        return self.reflector[self.base_alphabet.index(letter)]

    def encrypt_text(self, text: str):
        text = text.upper().replace(" ", "")

        encrypted_text = ""

        for letter in text:
            #print("PLUGBOARD OPS")
            temp = self.plugboard_operation(letter)
            #print("==============")
            #print("INBOUND ROTOR")
            temp = self.inbound_rotor(letter)
            #print("==============")
            #print("REFLECTOR")
            temp = self.reflector_operation(temp)
            #print("==============")
            #print("OUTBOUND ROTOR")
            temp = self.outbound_rotor(temp)
            self.turn_rotors()
            #print("==============")
            #print("PLUGBOARD OPS")
            temp = self.plugboard_operation(temp)
            encrypted_text += temp
            #print(f"curr setting: {self.rotor_pointers}")
            #print("\n")
        
        return encrypted_text