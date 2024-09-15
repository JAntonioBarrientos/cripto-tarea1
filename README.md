# Criptografía y seguridad Tarea1 implementaciones
Repositorio para mi implementación de cifrados, y herramientas para el criptoanálisis

- **Alumno**: José Antonio Barrientos Sánchez
- **No. Cuenta**: 423019269

Se necesitan las siguientes librerías para ejecutar los programas:

- numpy

## Instalación y activación de entorno virtual

Para instalar las librerías necesarias se necesita ejecutar el siguiente comando.

```bash
pip install -r requirements.txt
```

Para activar el entorno virtual se necesita ejecutar el siguiente comando.

```bash
source venv/bin/activate
```
Cambiar de directorio a la carpeta src.

```bash
cd src
```

Para ejecutar los programas se necesita escribir el siguiente comando.

```bash
python3 main.py
```

Si se quiere replicar la generación de los cifrados y descifrados se explica a continuación.

## Cifrado Afin

Para ejecutar el cifrado afin se necesita escribir el siguiente codigo.

```python
def main():

    ruta_archivo_entrada = 'docs/Texto1.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_cifrado_afin.txt'

    a = 11
    b = 8

    texto_cifrado = CifradoAfin.cifrar(texto, a, b, 'es')

    guardar_texto_en_archivo(texto_cifrado, ruta_archivo_salida)

```

Para descifrarlo se necesita escribir el siguiente codigo.

```python
def main():
    ruta_archivo_entrada = 'docs/Texto1_cifrado_afin.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_descifrado_afin.txt'

    a = 11
    b = 8

    texto_descifrado = CifradoAfin.descifrar(texto, a, b, 'es')

    guardar_texto_en_archivo(texto_descifrado, ruta_archivo_salida)
```

## Cifrado Hill

Para ejecutar el cifrado Hill se necesita escribir el siguiente codigo.

```python
def main():

    ruta_archivo_entrada = 'docs/Texto1.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_cifrado_hill.txt'

    
    # Matriz clave 2x2 para el cifrado de Hill
    key_matrix = [[5, 7], [11, 3]]

    # Crear una instancia del cifrado de Hill
    cipher = HillCipher(key_matrix)


    # Cifrar
    ciphertext = cipher.encrypt(texto)
    guardar_texto_en_archivo(ciphertext, ruta_archivo_salida)
```

Para descifrarlo se necesita escribir el siguiente codigo.

```python
def main():
    ruta_archivo_entrada = 'docs/Texto1_cifrado_hill.txt'

    texto = leer_archivo(ruta_archivo_entrada)

    ruta_archivo_salida = 'docs/Texto1_descifrado_hill.txt'

    # Matriz clave 2x2 para el cifrado de Hill
    key_matrix = [[5, 7], [11, 3]]

    # Crear una instancia del cifrado de Hill
    cipher = HillCipher(key_matrix)

    # Descifrar
    plaintext = cipher.decrypt(texto)
    guardar_texto_en_archivo(plaintext, ruta_archivo_salida)
```
