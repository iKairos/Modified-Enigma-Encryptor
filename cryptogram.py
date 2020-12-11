import numpy as np
from matrix_cryptography import Matrix 

match = {" ": 0, "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
        "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23,
        "x": 24, "y": 25, "z": 26}

class Crypto:
    def convert(string: str):
        """
        Converts the message into its direct numerical form as per the dictionary 'match'. \n
        Parameter(s): \n
            > string (str): The message you wish to convert. \n
        Return value: Two dimensional list of the message's numerical value by three. \n \n
        """
        converted = []

        string = string.lower()

        try:
            for letter in string:
                converted.append(match[letter])
        except KeyError:
            print("[ERROR] Key error raised. Make sure your message's characters are included in the letter map.")
        
        processed = [converted[i:i+3] for i in range(0,len(converted),3)]

        if len(processed[len(processed)-1]) == 2:
            processed[len(processed)-1].append(0)
        elif len(processed[len(processed)-1]) == 1:
            processed[len(processed)-1].append(0)
            processed[len(processed)-1].append(0)
    
        return processed
    
    def encode(iterable: list, encoder: Matrix):
        """
        Encodes the message group by multiplying it to our encoder matrix. \n
        Parameter(s): \n
            > iterable (list): A two dimensional list which represents the converted message into its numerical values. \n
            > encoder (Matrix): The encoder matrix that will be used. \n
        Return value: Two dimensional list containing the encoded message.
        """
        encoded = []
        
        for code in iterable:
            ans = np.matmul(code, encoder.matrix_value())
            encoded.append(list(ans))
        
        return encoded

    def decode(iterable: list, decoder: Matrix):
        """
        Decodes the message by multiplying an encoded message to the inverse of the decoder matrix \n
        Parameter(s): \n
            > iterable (list): A two dimensional list which represents the encoded message. \n
            > decoder (Matrix): The encoded matrix but will be processed by calculating its inverse. \n
        Return value: Two dimensional list containing the decoded message.
        """
        decoded = []

        for code in iterable:
            ans = np.matmul(code, decoder.inverse())
            decoded.append(list(ans))
        
        return decoded
        