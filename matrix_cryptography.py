import numpy as np

class Matrix:
    """
    A class that withholds the information of a matrix.
    """
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
    
    def matrix_value(self):
        """
        Returns the value of the matrix itself. \n
        Return type: numpy array
        """
        return self.matrix
        
    def inverse(self):
        """
        Calculates the inverse of the matrix. \n
        Return type: numpy array
        """
        return np.linalg.inv(self.matrix)