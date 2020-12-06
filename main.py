from enigma import Enigma
from rotor_details import Rotors

if __name__ == "__main__":
    encryptor = Enigma(
        plugboard={"a": "c"},
        rotor_settings=['J', 'X', 'G']
    )

    #print(encryptor.settings)