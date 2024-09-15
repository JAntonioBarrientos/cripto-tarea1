import os
from utils_cipher import UtilsCipher
from affine_cipher import CifradoAfin

def leer_archivo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return file.read()

def guardar_texto_en_archivo(texto, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as file:
        file.write(texto)

def main():
    # Ruta de los archivos de entrada y salida
    ruta_archivo_entrada = 'Texto1.txt'
    ruta_archivo_salida = 'frecuencias.txt'

    
    # Ejemplo de uso
    texto = "Éste es un texto con signos de puntuación, acentos y espacios."
    a, b = 1, 2
    bandera = 'es'  # Usar alfabeto español con Ñ

    # Cifrar
    texto_cifrado = CifradoAfin.cifrar(texto, a, b, bandera)
    print("Texto Cifrado:")
    print(texto_cifrado)

    # Descifrar
    texto_descifrado = CifradoAfin.decifrar(texto_cifrado, a, b, bandera)
    print("Texto Descifrado:")
    print(texto_descifrado)

if __name__ == "__main__":
    main()
