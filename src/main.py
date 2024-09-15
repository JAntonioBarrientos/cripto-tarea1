import os
from utils_cipher import UtilsCipher
from mono_alf_cipher import CifradoMonoalfabeticoAleatorio
from vigenere_cipher import CifradoVigenere
from affine_cipher import CifradoAfin
from hill_cipher import HillCipher
import random

def leer_archivo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return file.read()

def guardar_texto_en_archivo(texto, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as file:
        file.write(texto)

def main():

    ruta_archivo_entrada = 'docs/Texto1.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_cifrado_hill.txt'

    
    # Matriz clave 2x2 para el cifrado de Hill
    key_matrix = [[5, 7], [11, 3]]

    # Crear una instancia del cifrado de Hill
    cipher = HillCipher(key_matrix)

    # Texto claro
    plaintext = "HELLO"

    # Cifrar
    ciphertext = cipher.encrypt(plaintext)
    print(f"Texto cifrado: {ciphertext}")

    # Descifrar
    decrypted_text = cipher.decrypt(ciphertext)

    guardar_texto_en_archivo(ciphertext, ruta_archivo_salida)

    print(f"Texto descifrado: {decrypted_text}")

    


if __name__ == "__main__":
    main()
