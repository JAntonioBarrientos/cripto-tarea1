from collections import Counter
import unicodedata

class UtilsCipher:
    @staticmethod
    def gcd(a, b):
        """
        Calcula el máximo común divisor de dos números usando el algoritmo de Euclides.
        
        :param a: Primer número.
        :param b: Segundo número.
        :return: El máximo común divisor de a y b.
        """
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def mod_inverse(a, m):
        """
        Calcula el inverso modular de 'a' bajo el módulo 'm' usando el algoritmo extendido de Euclides.
        
        :param a: El número del que se quiere obtener el inverso.
        :param m: El módulo.
        :return: El inverso modular de 'a' mod 'm' si existe, o None si no tiene inverso.
        """
        g, x, y = UtilsCipher.extended_gcd(a, m)
        if g != 1:
            return None  # No existe inverso
        else:
            return x % m

    @staticmethod
    def extended_gcd(a, b):
        """
        Algoritmo extendido de Euclides. Devuelve el GCD de a y b, junto con los coeficientes de Bezout.
        
        :param a: Primer número.
        :param b: Segundo número.
        :return: Una tupla (gcd, x, y) donde gcd es el máximo común divisor de a y b,
                 y x, y son los coeficientes de Bezout (ax + by = gcd(a, b)).
        """
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = UtilsCipher.extended_gcd(b % a, a)
            return (g, y - (b // a) * x, x)

    @staticmethod
    def remove_accents(text):
        """
        Elimina los acentos de las letras y las convierte en sus equivalentes sin acento.
        
        :param text: El texto original.
        :return: El texto sin acentos.
        """
        return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))

    @staticmethod
    def letter_frequencies(text):
        """
        Calcula la frecuencia de aparición de cada letra en un texto, y devuelve una tabla ordenada.
        Elimina acentos de letras acentuadas antes de calcular las frecuencias.
        
        :param text: El texto del que se quiere obtener la frecuencia de las letras.
        :return: Una tabla de string con la letra, frecuencia absoluta y frecuencia relativa.
        """
        # Remover acentos y filtrar solo letras, convertir a mayúsculas
        text = UtilsCipher.remove_accents(text.upper())
        text = ''.join(filter(str.isalpha, text))
        
        total_letters = len(text)
        
        # Usar Counter para contar las ocurrencias de cada letra
        frequencies = Counter(text)
        
        # Ordenar las letras por frecuencia, de mayor a menor
        sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        # Crear la tabla como un string
        table = "Letra | Frecuencia | Frecuencia Relativa\n"
        table += "-" * 40 + "\n"
        
        for letter, freq in sorted_frequencies:
            relative_freq = freq / total_letters
            table += f"{letter:^5} | {freq:^10} | {relative_freq:^18.4f}\n"
        
        return table


