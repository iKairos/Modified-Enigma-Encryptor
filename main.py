import json
from enigma import Enigma
from os import path

def init_menu():
    menu = "\nMENU: \n"
    menu += "1. New Enigma Instance\n"
    menu += "2. Process a Text\n"
    menu += "3. Set Key\n"
    menu += "4. Print Enigma Settings\n"
    menu += "5. Exit"

    print(menu)

if __name__ == "__main__":
    encryptor = None

    not_allowed = "\"[].!@#$%^&*()-+?_=,<>/\"\'\'1234567890"

    while True:
        print(f"\nCURRENT ROTOR SETTINGS: {'None' if encryptor is None else encryptor.settings}")
        print(f"\nCURRENT VIGENERE: {'None' if encryptor is None else encryptor.vigenere}")
        print(f"\nCURRENT MATRIX: {'None' if encryptor is None else encryptor.matrix_crypt}")

        init_menu()

        op = input("Select an option: ")
        print("\n")

        if op == '1':
            plugs = None 
            keys = None

            has_plugs = input("Do you have a custom plugboard wiring combination? (y/n)").lower()

            if has_plugs == 'y':
                file_dir = input("Specify the directory of the JSON plugboard combination: ")

                if path.isfile(file_dir):
                    with open(file_dir) as wirings:
                        plugboard_wirings = json.load(wirings)
                    
                        plugs = plugboard_wirings

                        break
                else:
                    print("Directory does not exist, try again.")
                    continue
            
            key_in = list(input("Please enter the key: "))

            if type(key_in) != list or len(key_in) != 18:
                print("Wrong key format, try again. (Default Settings Set)")
            else:
                keys = key_in
            
            encryptor = Enigma(plugs, rotor_settings=keys)
        
        elif op == '2':
            while True:
                ask = input("Encrypt or Decrypt? (e/d)")
                
                if ask == 'e':
                    enc = input("Enter a text to be encrypted: ")

                    if not any(char in not_allowed for char in enc):
                        text = encryptor.encrypt_text(enc.lower())

                        print(f"Encrypted text: {text}")
                    else:
                        print("Wrong plaintext format. Please make sure your plaintext does not contain any numbers or special characters.")
                    break
                elif ask == 'd':
                    dec = input("Enter a text to be decrypted: ")

                    if any(char.isnumeric() for char in dec.replace(" ", "")):
                        text = encryptor.decrypt_text(dec)

                        print(f"Decrypted text: {text}")
                    else:
                        print("Wrong format. Please try again.")

                    break
                else:
                    print("Wrong option, try again.")
        elif op == '3':
            if encryptor is None:
                print("Please create an enigma machine first.")
            else:
                keys = list(input("Please enter the key: "))

                if type(keys) != list or len(keys) != 18:
                    print("Wrong key format, try again.")
                else:
                    encryptor.set_rotor_settings(keys)
        
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