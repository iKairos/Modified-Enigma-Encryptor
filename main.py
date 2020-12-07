import json
from enigma import Enigma
from os import path

def init_menu():
    menu = "MENU: \n"
    menu += "1. New Enigma Instance\n"
    menu += "2. Process a Text\n"
    menu += "3. Set Rotor Positions\n"
    menu += "4. Print Enigma Settings"
    menu += "5. Exit"

    print(menu)

if __name__ == "__main__":
    encryptor = None

    while True:
        print(f"CURRENT ROTOR SETTINGS: {encryptor.settings}")
        init_menu()

        op = input("Select an option: ")

        if op == '1':
            encryptor = Enigma()

            has_plugs = True if input("Do you have a custom plugboard wiring combination? (y/n)").lower() == 'y' else False

            if has_plugs:
                while True:
                    file_dir = input("Specify the directory of the JSON plugboard combination: ")

                    if path.isfile(file_dir):
                        with open(file_dir) as wirings:
                            plugboard_wirings = json.loads(wirings)
                        
                            encryptor.set_plugboard_wiring(plugboard_wirings)
                    else:
                        print("Directory does not exist, try again.")
            
            has_rotors = True if input("Do you want to set the rotor settings manually? (y/n)").lower() == 'y' else False

            if has_rotors:
                rotors = input("Please enter rotor settings separated by commas per rotor: ").split(',')

                encryptor.set_rotor_settings(rotors)
        
        elif op == '2':
            enc = input("Enter a text to be encrypted: ")

            text = encryptor.encrypt_text(enc)

            print(f"Encrypted text: {text}")
