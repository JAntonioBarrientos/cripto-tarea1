import unicodedata
import string
from collections import Counter
from utils_cipher import UtilsCipher
import random

class CifradoVigenere:
    
    @staticmethod
    def preprocesar_texto(texto, bandera):
        """
        Preprocesa el texto eliminando acentos, signos de puntuación, espacios y convirtiéndolo a mayúsculas.
        En caso de 'en', reemplaza 'Ñ' por 'N'.
        
        :param texto: El texto a preprocesar.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto preprocesado listo para cifrar/descifrar.
        """
        # Elimina acentos y normaliza
        texto = CifradoVigenere.eliminar_acentos(texto, bandera)
        
        # Elimina signos de puntuación y espacios
        texto = ''.join(filter(str.isalpha, texto)).upper()
        
        # Si se usa el alfabeto en inglés, convertir Ñ a N
        if bandera == 'en':
            texto = texto.replace('Ñ', 'N')
        
        return texto

    @staticmethod
    def eliminar_acentos(texto, bandera):
        """
        Función auxiliar que elimina acentos de las letras. 
        Si la bandera es 'es', preserva la 'Ñ'.
        
        :param texto: El texto a procesar.
        :param bandera: 'es' para español, 'en' para inglés.
        :return: Texto sin acentos.
        """
        # Si estamos trabajando con español, preservamos la Ñ
        if bandera == 'es':
            texto = texto.replace('Ñ', '__TEMP_N__').replace('ñ', '__temp_n__')
            
        # Elimina los acentos de las demás letras
        texto = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
        
        # Restaurar la Ñ
        if bandera == 'es':
            texto = texto.replace('__TEMP_N__', 'Ñ').replace('__temp_n__', 'ñ')
            
        return texto


    @staticmethod
    def obtener_alfabeto(bandera):
        """
        Obtiene el alfabeto correspondiente dependiendo de la bandera.
        
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El alfabeto a usar.
        """
        if bandera == 'es':
            # Alfabeto en español con la Ñ en la posición correcta
            return 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        else:
            # Alfabeto inglés
            return string.ascii_uppercase

    @staticmethod
    def cifrar(texto, clave, bandera):
        """
        Cifra el texto usando el cifrado Vigenère.
        
        :param texto: El texto a cifrar.
        :param clave: La clave utilizada para cifrar.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto cifrado.
        """
        texto = CifradoVigenere.preprocesar_texto(texto, bandera)
        clave = CifradoVigenere.preprocesar_texto(clave, bandera)
        alfabeto = CifradoVigenere.obtener_alfabeto(bandera)
        N = len(alfabeto)
        
        texto_cifrado = ''
        indice_clave = 0

        for letra in texto:
            # Obtenemos el valor de la letra de la clave
            valor_clave = alfabeto.index(clave[indice_clave % len(clave)])
            # Cifrado Vigenère: (x + y) % N, donde x es el valor de la letra y y es el valor de la clave
            valor_letra = (alfabeto.index(letra) + valor_clave) % N
            texto_cifrado += alfabeto[valor_letra]
            indice_clave += 1

        return texto_cifrado

    @staticmethod
    def descifrar(texto_cifrado, clave, bandera):
        """
        Descifra el texto usando el descifrado Vigenère.
        
        :param texto_cifrado: El texto cifrado.
        :param clave: La clave utilizada para descifrar.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto descifrado en bloques de 10 letras.
        """
        # Preprocesar el texto cifrado y la clave
        texto_cifrado = CifradoVigenere.preprocesar_texto(texto_cifrado, bandera)
        clave = CifradoVigenere.preprocesar_texto(clave, bandera)
        alfabeto = CifradoVigenere.obtener_alfabeto(bandera)
        N = len(alfabeto)

        texto_descifrado = ''
        indice_clave = 0

        for letra in texto_cifrado:
            # Obtenemos el valor de la letra de la clave
            valor_clave = alfabeto.index(clave[indice_clave % len(clave)])
            # Descifrado Vigenère: (x - y) % N, donde x es el valor de la letra cifrada y y es el valor de la clave
            valor_letra = (alfabeto.index(letra) - valor_clave) % N
            texto_descifrado += alfabeto[valor_letra]
            indice_clave += 1

        # Dividir el texto descifrado en bloques de 10 letras
        return ' '.join([texto_descifrado[i:i+10] for i in range(0, len(texto_descifrado), 10)])


    @staticmethod
    def indice_coincidencia(texto, bandera = 'en'):
        """
        Calcula el índice de coincidencia de un texto dado, eliminando acentos y procesando correctamente el texto.
        
        :param texto: El texto sobre el cual calcular el índice de coincidencia.
        :return: El valor del índice de coincidencia.
        """
        # Eliminar acentos y procesar el texto para convertirlo a mayúsculas y eliminar caracteres no alfabéticos
        texto = CifradoVigenere.eliminar_acentos(texto, bandera)
        texto = ''.join(filter(str.isalpha, texto.upper()))
        
        # Obtener la frecuencia de cada letra
        frecuencias = Counter(texto)
        N = len(texto)  # Longitud del texto
        
        # Aplicar la fórmula del índice de coincidencia
        suma_frecuencias = sum(f * (f - 1) for f in frecuencias.values())
        ic = suma_frecuencias / (N * (N - 1)) if N > 1 else 0
        
        return round(ic, 5)

    @staticmethod
    def generar_clave_aleatoria(l, r):
        """
        Genera una clave aleatoria de longitud l usando r letras distintas del alfabeto inglés (A-Z).
        
        :param l: Longitud de la clave.
        :param r: Número de letras distintas.
        :return: Clave aleatoria de longitud l.
        """
        alfabeto_en = string.ascii_uppercase
        
        # Seleccionar r letras distintas del alfabeto inglés
        letras_distintas = random.sample(alfabeto_en, r)
        
        # Generar una clave de longitud l mezclando las letras distintas
        clave = ''.join(random.choice(letras_distintas) for _ in range(l))
        
        return clave

    @staticmethod
    def generar_tabla_ic(texto, longitudes, rs):
        """
        Genera una tabla de índices de coincidencia para diferentes longitudes de clave (l) y número de alfabetos usados (r).
        
        :param texto: El texto sobre el cual calcular el índice de coincidencia.
        :param longitudes: Lista de longitudes de clave (l).
        :param rs: Lista de números de alfabetos usados (r).
        :return: Un string que representa la tabla con los índices de coincidencia redondeados a 5 decimales.
        """
        # Definir el alfabeto inglés
        alfabeto_en = string.ascii_uppercase
        
        # Inicializar la tabla
        tabla = []
        
        for l in longitudes:
            fila = []
            for r in rs:
                # Generar clave aleatoria de longitud l
                clave = CifradoVigenere.generar_clave_aleatoria(l, r)
                
                # Calcular el índice de coincidencia para el texto cifrado con la clave generada
                ic = CifradoVigenere.indice_coincidencia(clave)
                fila.append(ic)
            tabla.append(fila)
        
        # Devolver la tabla como un string
        return CifradoVigenere.formatear_tabla(tabla, longitudes, rs)

    @staticmethod
    def formatear_tabla(tabla, longitudes, rs):
        """
        Formatea la tabla de índices de coincidencia en un string.
        
        :param tabla: La tabla de índices de coincidencia.
        :param longitudes: Lista de longitudes de clave (l).
        :param rs: Lista de números de alfabetos usados (r).
        :return: Un string que representa la tabla con los índices de coincidencia.
        """
        # Construir el encabezado
        encabezado = "| l \\ r | " + " | ".join(map(str, rs)) + " |"
        separador = "-" * len(encabezado)
        
        # Construir la tabla como string
        resultado = [encabezado, separador]
        
        for i, fila in enumerate(tabla):
            fila_string = "|  {}  | ".format(longitudes[i]) + " | ".join(f"{ic:.5f}" for ic in fila) + " |"
            resultado.append(fila_string)
            resultado.append(separador)
        
        # Devolver el string completo
        return "\n".join(resultado)
