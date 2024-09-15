import random
import string

class CifradoMonoalfabeticoAleatorio:
    
    @staticmethod
    def generar_clave():
        """
        Genera una clave aleatoria para el cifrado monoalfabético aleatorio.
        La clave es una permutación del alfabeto de 26 letras (A-Z).
        
        :return: Una clave aleatoria como string.
        """
        alfabeto = list(string.ascii_uppercase)
        random.shuffle(alfabeto)  # Permutar aleatoriamente las letras
        return ''.join(alfabeto)

    @staticmethod
    def preprocesar_texto(texto):
        """
        Preprocesa el texto eliminando signos de puntuación, espacios y convierte a mayúsculas.
        
        :param texto: El texto a preprocesar.
        :return: El texto preprocesado listo para cifrar/descifrar.
        """
        # Eliminar signos de puntuación y espacios, convertir a mayúsculas
        texto = ''.join(filter(str.isalpha, texto)).upper()
        return texto

    @staticmethod
    def cifrar(texto, clave):
        """
        Cifra el texto usando un cifrado monoalfabético aleatorio.
        
        :param texto: El texto a cifrar.
        :param clave: Una cadena de 26 letras que representa la clave de cifrado.
        :return: El texto cifrado.
        """
        texto = CifradoMonoalfabeticoAleatorio.preprocesar_texto(texto)
        alfabeto = string.ascii_uppercase  # Alfabeto estándar de A-Z
        mapeo = {alfabeto[i]: clave[i] for i in range(26)}  # Crear mapeo letra -> letra clave
        
        # Cifrar cada letra del texto
        texto_cifrado = ''.join([mapeo[letra] for letra in texto])
        
        # Dividir en bloques de 10 letras
        return ' '.join([texto_cifrado[i:i+10] for i in range(0, len(texto_cifrado), 10)])

    @staticmethod
    def descifrar(texto_cifrado, clave):
        """
        Descifra un texto usando un cifrado monoalfabético aleatorio.
        
        :param texto_cifrado: El texto cifrado a descifrar.
        :param clave: Una cadena de 26 letras que representa la clave de cifrado.
        :return: El texto descifrado.
        """
        texto_cifrado = CifradoMonoalfabeticoAleatorio.preprocesar_texto(texto_cifrado)
        alfabeto = string.ascii_uppercase
        mapeo_inverso = {clave[i]: alfabeto[i] for i in range(26)}

        # Descifrar cada letra del texto
        texto_descifrado = ''.join([mapeo_inverso[letra] for letra in texto_cifrado])
        
        # Dividir en bloques de 10 letras
        return ' '.join([texto_descifrado[i:i+10] for i in range(0, len(texto_descifrado), 10)])

    @staticmethod
    def descifrar_con_mapeo_parcial(texto_cifrado, mapeo_parcial):
        """
        Descifra un texto usando un mapeo parcial, donde solo algunas letras están mapeadas.
        Las letras que no estén mapeadas se reemplazan por '_'.
        
        :param texto_cifrado: El texto cifrado a descifrar.
        :param mapeo_parcial: Un diccionario con mapeos parciales de letras cifradas a letras descifradas.
        :return: El texto descifrado con las letras no mapeadas reemplazadas por '_'.
        """
        texto_cifrado = CifradoMonoalfabeticoAleatorio.preprocesar_texto(texto_cifrado)
        
        # Descifrar utilizando el mapeo parcial, y sustituir por '_' si no existe un mapeo
        texto_descifrado = ''.join([mapeo_parcial.get(letra, '_') for letra in texto_cifrado])
        
        # Dividir en bloques de 10 letras
        return ' '.join([texto_descifrado[i:i+10] for i in range(0, len(texto_descifrado), 10)])


