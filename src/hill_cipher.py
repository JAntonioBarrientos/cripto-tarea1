import numpy as np
from utils_cipher import UtilsCipher
import unicodedata

class HillCipher:
    def __init__(self, key_matrix):
        """
        Inicializa el cifrado de Hill con una matriz clave de 2x2.
        
        :param key_matrix: Matriz clave 2x2.
        """
        if len(key_matrix) != 2 or len(key_matrix[0]) != 2 or len(key_matrix[1]) != 2:
            raise ValueError("La matriz clave debe ser de tamaño 2x2.")
        self.key_matrix = np.array(key_matrix)
        self.modulus = 27  # Para incluir A-Z y Ñ

    @staticmethod
    def eliminar_acentos(texto):
        """
        Elimina acentos y normaliza el texto.
        """
        return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

    @staticmethod
    def preprocesar_texto(texto):
        """
        Preprocesa el texto eliminando espacios, puntuación, acentos y lo convierte a mayúsculas.
        """
        texto = HillCipher.eliminar_acentos(texto)
        texto = ''.join(filter(str.isalpha, texto.upper()))
        return texto.replace('Ñ', 'Ñ')  # La ñ sigue siendo "Ñ"

    @staticmethod
    def text_to_numbers(text):
        """
        Convierte el texto a una lista de números (A=0, B=1, ..., Ñ=14, Z=26).
        
        :param text: El texto a convertir.
        :return: Lista de números correspondientes al texto.
        """
        alphabet = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        return [alphabet.index(char) for char in text]

    @staticmethod
    def numbers_to_text(numbers):
        """
        Convierte una lista de números de vuelta a texto (0=A, 1=B, ..., Ñ=14, Z=26).
        
        :param numbers: Lista de números para convertir a texto.
        :return: El texto correspondiente.
        """
        alphabet = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        return ''.join([alphabet[num] for num in numbers])

    @staticmethod
    def determinante_2x2(matrix):
        """
        Calcula el determinante de una matriz 2x2.
        
        :param matrix: Matriz 2x2.
        :return: Determinante de la matriz.
        """
        return int(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])

    def mod_inverse_matrix(self, matrix, modulus):
        """
        Calcula la inversa de una matriz 2x2 módulo `modulus`.
        
        :param matrix: La matriz para invertir.
        :param modulus: El valor del módulo.
        :return: La matriz inversa módulo `modulus`, o None si no existe.
        """
        det = self.determinante_2x2(matrix)
        det_inv = UtilsCipher.mod_inverse(det % 27, modulus)  # Inverso modular del determinante

        if det_inv is None:
            raise ValueError("La matriz no tiene inversa en Z{}".format(modulus))

        # Matriz adjunta (intercambiar diagonal y cambiar signos fuera de la diagonal)
        adjugate_matrix = np.array([[matrix[1][1], -matrix[0][1]], 
                                    [-matrix[1][0], matrix[0][0]]]) % modulus

        # Matriz inversa = adjunta * inverso del determinante (mod modulus)
        return (det_inv * adjugate_matrix) % modulus

    def encrypt(self, plaintext):
        """
        Cifra el texto claro utilizando el cifrado de Hill con matriz clave 2x2.
        
        :param plaintext: El texto claro.
        :return: El texto cifrado.
        """
        plaintext = self.preprocesar_texto(plaintext)
        plaintext_numbers = self.text_to_numbers(plaintext)

        # Añadir padding si es necesario para que la longitud sea múltiplo de 2
        if len(plaintext_numbers) % 2 != 0:
            plaintext_numbers.append(24)  # Padding con X (que corresponde a 0)

        # Dividir el texto en bloques de tamaño 2 y cifrar cada bloque
        ciphertext_numbers = []
        for i in range(0, len(plaintext_numbers), 2):
            block = np.array(plaintext_numbers[i:i + 2])
            cipher_block = np.dot(self.key_matrix, block) % self.modulus
            ciphertext_numbers.extend(cipher_block)

        return self.numbers_to_text(ciphertext_numbers)

    def decrypt(self, ciphertext):
        """
        Descifra el texto cifrado utilizando el cifrado de Hill con matriz clave 2x2.
        
        :param ciphertext: El texto cifrado.
        :return: El texto claro.
        """
        ciphertext = self.preprocesar_texto(ciphertext)
        ciphertext_numbers = self.text_to_numbers(ciphertext)

        # Calcular la inversa de la matriz clave en Z27
        key_matrix_inv = self.mod_inverse_matrix(self.key_matrix, self.modulus)

        # Dividir el texto en bloques de tamaño 2 y descifrar cada bloque
        plaintext_numbers = []
        for i in range(0, len(ciphertext_numbers), 2):
            block = np.array(ciphertext_numbers[i:i + 2])
            plain_block = np.dot(key_matrix_inv, block) % self.modulus
            plaintext_numbers.extend(plain_block)

        return self.numbers_to_text(plaintext_numbers)
