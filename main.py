import json
from enigma import Enigma
from os import path

def init_menu():
    menu = "\nMENU: \n"
    menu += "1. New Enigma Instance\n"
    menu += "2. Process a Text\n"
    menu += "3. Set Rotor Positions\n"
    menu += "4. Print Enigma Settings\n"
    menu += "5. Exit"

    print(menu)

if __name__ == "__main__":
    encryptor = None

    while True:
        print(f"\nCURRENT ROTOR SETTINGS: {'None' if encryptor is None else encryptor.settings}")
        print(f"\nCURRENT VIGENERE: {'None' if encryptor is None else encryptor.vigenere}")

        init_menu()

        op = input("Select an option: ")
        print("\n")

        if op == '1':
            encryptor = Enigma()

            has_plugs = True if input("Do you have a custom plugboard wiring combination? (y/n)").lower() == 'y' else False

            if has_plugs:
                while True:
                    file_dir = input("Specify the directory of the JSON plugboard combination: ")

                    if path.isfile(file_dir):
                        with open(file_dir) as wirings:
                            plugboard_wirings = json.load(wirings)
                        
                            encryptor.set_plugboard_wiring(plugboard_wirings)

                            break
                    else:
                        print("Directory does not exist, try again.")
            
            keys = input("Please enter keys separated by commas: ").split(',')

            encryptor.set_rotor_settings(keys)
        
        elif op == '2':
            ask = input("Encrypt of Decrypt? (e/d) ").lower()

            while True:
                if ask == 'e':
                    enc = input("Enter a text to be encrypted: ")

                    text = encryptor.encrypt_text(enc)

                    print(f"Encrypted text: {text}")
                    
                    break
                elif ask == 'd':
                    dec = input("Enter a text to be encrypted: ")

                    text = encryptor.decrypt_text(dec)

                    print(f"Decrypted text: {text}")

                    break
                else:
                    print("Wrong option, try again.")
        elif op == '3':
            if encryptor is None:
                print("Please create an enigma machine first.")
            else:
                rotors = input("Please enter rotor settings separated by commas per rotor: ").split(',')

                encryptor.set_rotor_settings(rotors)
        
        elif op == '4':
            if encryptor is None:
                print("Please create an enigma machine first.")
            else:
                print("Enigma Settings:\n")
                print(f"\tRotor Settings: {encryptor.settings}\n")
                print(f"\tCurrent Rotor Pointer: {encryptor.rotor_pointer_settings}\n")
                print(f"\tPlugboard: {encryptor.plugboard}\n")
        
        elif op == '5':
            break

        print("============================")