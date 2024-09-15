import string
import unicodedata
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
        texto = CifradoAfin.eliminar_acentos(texto)
        
        # Elimina signos de puntuación y espacios
        texto = ''.join(filter(str.isalpha, texto)).upper()
        
        # Si se usa el alfabeto en inglés, convertir Ñ a N
        if bandera == 'en':
            texto = texto.replace('Ñ', 'N')
        
        return texto

    @staticmethod
    def eliminar_acentos(texto):
        """
        Función auxiliar que elimina acentos de las letras.
        
        :param texto: El texto a procesar.
        :return: Texto sin acentos.
        """
        return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

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
    def decifrar(texto, a, b, bandera):
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


