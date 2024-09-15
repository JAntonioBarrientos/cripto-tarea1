import re

class PlayfairCipher:
    def __init__(self):
        # Definimos la matriz de Playfair proporcionada
        self.matriz = [
            ['E', 'A', 'J', 'S', 'Z'],
            ['L', 'C', 'K', 'T', 'I'],
            ['D', 'M', 'U', 'B', 'F'],
            ['N', 'V', 'R', 'G', 'P'],
            ['X', 'O', 'H', 'Q', 'Y']  # 'W' treated as 'X'
        ]
    
    def preprocesar_texto(self, texto):
        """
        Preprocesa el texto eliminando signos de puntuación, cambiando Ñ por N, W por X, y eliminando espacios.
        """
        # Eliminar signos de puntuación y convertir a mayúsculas
        texto = re.sub(r'[^A-ZÑ]', '', texto.upper())  # Mantener solo letras mayúsculas y Ñ
        texto = texto.replace('Ñ', 'N').replace('W', 'X')  # Tratar Ñ como N, W como X
        
        # Añadir 'X' entre letras repetidas en un dígrafo (por ejemplo, "AA" -> "AXA")
        texto_procesado = ''
        i = 0
        while i < len(texto):
            texto_procesado += texto[i]
            if i + 1 < len(texto) and texto[i] == texto[i + 1]:
                texto_procesado += 'X'
            i += 1

        # Si la longitud es impar, añadir 'X' al final
        if len(texto_procesado) % 2 != 0:
            texto_procesado += 'X'
        
        return texto_procesado
    
    def obtener_posicion(self, letra):
        """
        Obtiene la posición (fila, columna) de una letra en la matriz de Playfair.
        Lanza una excepción si la letra no se encuentra.
        """
        for fila in range(5):
            for columna in range(5):
                if self.matriz[fila][columna] == letra:
                    return fila, columna
        raise ValueError(f"La letra '{letra}' no se encuentra en la matriz de Playfair.")

    def cifrar_digrama(self, letra1, letra2):
        """
        Cifra un dígrama usando las reglas de Playfair.
        """
        fila1, col1 = self.obtener_posicion(letra1)
        fila2, col2 = self.obtener_posicion(letra2)

        # Caso 1: Ambas letras en la misma fila
        if fila1 == fila2:
            return self.matriz[fila1][(col1 + 1) % 5] + self.matriz[fila2][(col2 + 1) % 5]

        # Caso 2: Ambas letras en la misma columna
        elif col1 == col2:
            return self.matriz[(fila1 + 1) % 5][col1] + self.matriz[(fila2 + 1) % 5][col2]

        # Caso 3: Letras forman un rectángulo
        else:
            return self.matriz[fila1][col2] + self.matriz[fila2][col1]

    def cifrar(self, texto):
        """
        Cifra el texto usando el cifrado Playfair.
        """
        texto = self.preprocesar_texto(texto)
        criptotexto = ''

        # Dividir el texto en dígrafos
        for i in range(0, len(texto), 2):
            letra1, letra2 = texto[i], texto[i + 1]
            criptotexto += self.cifrar_digrama(letra1, letra2)

        return criptotexto

    def descifrar_digrama(self, letra1, letra2):
        """
        Descifra un dígrama usando las reglas de Playfair.
        """
        fila1, col1 = self.obtener_posicion(letra1)
        fila2, col2 = self.obtener_posicion(letra2)

        # Caso 1: Ambas letras en la misma fila
        if fila1 == fila2:
            return self.matriz[fila1][(col1 - 1) % 5] + self.matriz[fila2][(col2 - 1) % 5]

        # Caso 2: Ambas letras en la misma columna
        elif col1 == col2:
            return self.matriz[(fila1 - 1) % 5][col1] + self.matriz[(fila2 - 1) % 5][col2]

        # Caso 3: Letras forman un rectángulo
        else:
            return self.matriz[fila1][col2] + self.matriz[fila2][col1]

    def descifrar(self, texto_cifrado):
        """
        Descifra el texto cifrado usando el cifrado Playfair.
        """
        texto_cifrado = self.preprocesar_texto(texto_cifrado)
        texto_claro = ''

        # Dividir el texto cifrado en dígrafos
        for i in range(0, len(texto_cifrado), 2):
            letra1, letra2 = texto_cifrado[i], texto_cifrado[i + 1]
            texto_claro += self.descifrar_digrama(letra1, letra2)

        return texto_claro
