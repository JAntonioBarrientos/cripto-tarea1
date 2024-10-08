import os
from utils_cipher import UtilsCipher
from mono_alf_cipher import CifradoMonoalfabeticoAleatorio
from vigenere_cipher import CifradoVigenere
from affine_cipher import CifradoAfin
from hill_cipher import HillCipher
from playfair_cipher import PlayfairCipher
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
    ruta_archivo_entrada = 'docs/Texto1_cifrado_playfair.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_descifrado_playfair.txt'

    cipher = PlayfairCipher()
    plaintext = cipher.descifrar(texto)

    guardar_texto_en_archivo(plaintext, ruta_archivo_salida)


if __name__ == "__main__":
    main()
