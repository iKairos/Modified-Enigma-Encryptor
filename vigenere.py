# A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z  
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25

class Vigenere:
    def __init__(self, key_code):
        self.key_code = key_code

    def encrypt(self, plain_text):
        encrypted_text = ''

        if plain_text == ' ':
            encrypted_text = plain_text

        elif plain_text == ',':
            encrypted_text = plain_text

        else:
            number = ord(plain_text.upper()) + self.key_code
            if number > 90:
                number -= 26
            encrypted_text = chr(number)

        return encrypted_text

    def decrypt(self, plain_text):
        decrypted_text = ''

        if plain_text == ' ':
            decrypted_text = plain_text

        elif plain_text == ',':
            decrypted_text = plain_text

        else:
            number = ord(plain_text.upper()) - self.key_code
            if number < 64:
                number += 26
            decrypted_text = chr(number)
    
        return decrypted_text