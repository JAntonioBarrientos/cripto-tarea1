import numpy as np
from collections import Counter

class HillCipher:
    def __init__(self, key_matrix):
        """
        Inicializa el cifrado de Hill con la matriz clave.
        
        :param key_matrix: La matriz clave usada para cifrar el texto (debe ser invertible modulo 26).
        """
        self.key_matrix = np.array(key_matrix)
        self.n = self.key_matrix.shape[0]  # Tamaño de la matriz (n x n)
        self.modulus = 26  # Para el cifrado Hill, usamos el alfabeto inglés de 26 letras

    @staticmethod
    def mod_inverse_matrix(matrix, modulus):
        """
        Calcula la inversa de una matriz modulo un número dado.
        
        :param matrix: La matriz para invertir.
        :param modulus: El valor del módulo (en este caso, 26).
        :return: La matriz inversa modulo `modulus`, o None si no existe.
        """
        det = int(np.round(np.linalg.det(matrix)))  # Determinante de la matriz
        det_mod_inv = UtilsCipher.mod_inverse(det, modulus)  # Inverso modular del determinante

        if det_mod_inv is None:
            raise ValueError("La matriz no tiene inversa en Z26 (determinante no coprimo con 26)")

        # Calcular la matriz adjunta (cofactors matrix transpuesta)
        adjugate_matrix = np.round(np.linalg.det(matrix) * np.linalg.inv(matrix)).astype(int) % modulus
        inverse_matrix = (det_mod_inv * adjugate_matrix) % modulus

        return inverse_matrix

    @staticmethod
    def text_to_numbers(text):
        """
        Convierte el texto a una lista de números (A=0, B=1, ..., Z=25).
        
        :param text: El texto a convertir.
        :return: La lista de números correspondientes al texto.
        """
        text = text.upper().replace('Ñ', 'N')  # En inglés no se usa Ñ
        return [(ord(char) - ord('A')) % 26 for char in text if char.isalpha()]

    @staticmethod
    def numbers_to_text(numbers):
        """
        Convierte una lista de números de vuelta a texto (0=A, 1=B, ..., 25=Z).
        
        :param numbers: Lista de números para convertir a texto.
        :return: El texto correspondiente.
        """
        return ''.join([chr(num + ord('A')) for num in numbers])

    def encrypt(self, plaintext):
        """
        Cifra el texto claro utilizando el cifrado de Hill.
        
        :param plaintext: El texto claro.
        :return: El texto cifrado.
        """
        plaintext_numbers = self.text_to_numbers(plaintext)

        # Añadir padding si es necesario para que la longitud sea múltiplo de n
        while len(plaintext_numbers) % self.n != 0:
            plaintext_numbers.append(0)  # Padding con A (que corresponde a 0)

        # Dividir el texto en bloques de tamaño n y cifrar cada bloque
        ciphertext_numbers = []
        for i in range(0, len(plaintext_numbers), self.n):
            block = np.array(plaintext_numbers[i:i + self.n])
            cipher_block = np.dot(self.key_matrix, block) % self.modulus
            ciphertext_numbers.extend(cipher_block)

        return self.numbers_to_text(ciphertext_numbers)

    def decrypt(self, ciphertext):
        """
        Descifra el texto cifrado utilizando el cifrado de Hill.
        
        :param ciphertext: El texto cifrado.
        :return: El texto claro.
        """
        ciphertext_numbers = self.text_to_numbers(ciphertext)

        # Calcular la inversa de la matriz clave en Z26
        key_matrix_inv = self.mod_inverse_matrix(self.key_matrix, self.modulus)

        # Dividir el texto en bloques y descifrar cada bloque
        plaintext_numbers = []
        for i in range(0, len(ciphertext_numbers), self.n):
            block = np.array(ciphertext_numbers[i:i + self.n])
            plain_block = np.dot(key_matrix_inv, block) % self.modulus
            plaintext_numbers.extend(plain_block)

        return self.numbers_to_text(plaintext_numbers)
