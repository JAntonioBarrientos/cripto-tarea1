import string
import unicodedata
from collections import Counter
from utils_cipher import UtilsCipher  

class CifradoAfin:
    @staticmethod
    def preprocesar_texto(texto, bandera):
        """
        Preprocesa el texto eliminando acentos, signos de puntuación, espacios, y convierte a mayúsculas.
        En caso de 'en', reemplaza 'Ñ' por 'N'.
        
        :param texto: El texto a preprocesar.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto preprocesado listo para cifrar/descifrar.
        """
        # Elimina acentos y normaliza
        texto = CifradoAfin.eliminar_acentos(texto, bandera)
        
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
    def cifrar(texto, a, b, bandera):
        """
        Cifra el texto usando el cifrado afín: (a * x + b) mod N.
        
        :param texto: El texto a cifrar.
        :param a: El valor de a en la fórmula afín.
        :param b: El valor de b en la fórmula afín.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto cifrado en bloques de 10 letras.
        """
        texto = CifradoAfin.preprocesar_texto(texto, bandera)
        alfabeto = CifradoAfin.obtener_alfabeto(bandera)
        N = len(alfabeto)
        
        # Cifrado afín: (a * x + b) mod N
        texto_cifrado = ''.join([alfabeto[(a * alfabeto.index(letra) + b) % N] for letra in texto])
        
        # Dividir en bloques de 10 letras
        return ' '.join([texto_cifrado[i:i+10] for i in range(0, len(texto_cifrado), 10)])

    @staticmethod
    def descifrar(texto, a, b, bandera):
        """
        Descifra el texto usando el descifrado afín: a_inv * (x - b) mod N.
        
        :param texto: El texto a descifrar.
        :param a: El valor de a en la fórmula afín.
        :param b: El valor de b en la fórmula afín.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: El texto descifrado en bloques de 10 letras.
        """
        texto = CifradoAfin.preprocesar_texto(texto, bandera)
        alfabeto = CifradoAfin.obtener_alfabeto(bandera)
        N = len(alfabeto)
        
        # Obtener el inverso multiplicativo de 'a' en mod N
        a_inv = UtilsCipher.mod_inverse(a, N)
        if a_inv is None:
            raise ValueError(f"No existe inverso multiplicativo de {a} mod {N}")
        
        # Descifrado afín: a_inv * (x - b) mod N
        texto_descifrado = ''.join([alfabeto[a_inv * (alfabeto.index(letra) - b) % N] for letra in texto])
        
        # Dividir en bloques de 10 letras
        return ' '.join([texto_descifrado[i:i+10] for i in range(0, len(texto_descifrado), 10)])

    @staticmethod
    def fuerza_bruta(texto_cifrado, bandera):
        """
        Rompe el cifrado afín usando fuerza bruta probando todas las combinaciones de 'a' y 'b'.
        Devuelve los primeros 100 caracteres de los resultados posibles como un solo string formateado.
        
        :param texto_cifrado: El texto cifrado que se va a romper.
        :param bandera: 'es' para español (alfabeto con Ñ), 'en' para inglés (sin Ñ).
        :return: Un string con todas las combinaciones de 'a', 'b' y los primeros 100 caracteres de los textos descifrados.
        """
        alfabeto = CifradoAfin.obtener_alfabeto(bandera)
        N = len(alfabeto)

        resultados = []  # Lista para almacenar los resultados

        # Probar todas las combinaciones posibles de 'a' y 'b'
        for a in range(1, N):
            if UtilsCipher.gcd(a, N) == 1:  # Solo probar valores de 'a' coprimos con N
                for b in range(N):
                    try:
                        texto_descifrado = CifradoAfin.descifrar(texto_cifrado, a, b, bandera)
                        # Tomar solo los primeros 100 caracteres del texto descifrado
                        texto_descifrado_truncado = texto_descifrado[:100]
                        # Formatear la salida y agregarla a la lista de resultados
                        resultados.append(f"a = {a}, b = {b}\n{texto_descifrado_truncado}\n")
                    except ValueError:
                        continue

        # Devolver todos los resultados como un solo string
        return ''.join(resultados)
