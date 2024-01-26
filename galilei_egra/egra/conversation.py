from difflib import SequenceMatcher
import re

def comparar_textos(original, leido_por_nino):
    # Tokenizar los textos en palabras
    palabras_originales = original.split()
    palabras_leidas = leido_por_nino.split()

    # Calcular el número de palabras en cada texto
    num_palabras_originales = len(palabras_originales)
    num_palabras_leidas = len(palabras_leidas)

    # Calcular el número de aciertos utilizando SequenceMatcher
    comparador = SequenceMatcher(None, palabras_originales, palabras_leidas)
    aciertos = comparador.find_longest_match(0, num_palabras_originales, 0, num_palabras_leidas).size

    return num_palabras_originales, num_palabras_leidas, aciertos

def CompareFromText(texto_leido):
    # Ejemplo de uso
    texto_original =  re.sub(r'[^a-zA-Z0-9áéíóúü ]', '', "María tiene una gata. A la gata le gusta jugar. Un día María no encontró a su gata. María y su mamá la buscaron por toda la casa. De pronto oyeron “miau, miau”. Los maullidos eran suaves. Venían de debajo de la cama. María y su mamá encontraron a la gata y dos gatitos. La gata de María tuvo gatitos. La mamá de María le dijo: Yo también tendré un bebé. Vas a tener un hermanito. María sonrió y se fue corriendo a la casa de su amiga lorena. Al llegar le dijo a Lorena: “Vengo a contarte grandes noticias").lower()
    texto_leido_por_nino = texto_leido
    print("Texto Original: "+texto_original)
    print("Texto Niño: "+texto_leido_por_nino)
    num_palabras_originales, num_palabras_leidas, aciertos = comparar_textos(texto_original, texto_leido_por_nino)

    print(f"Número de palabras en el texto original: {num_palabras_originales}")
    print(f"Número de palabras en el texto leído por el niño: {num_palabras_leidas}")
    print(f"Número de aciertos: {aciertos}")

    return {"Número de palabras en el texto original":num_palabras_originales, "Número de palabras en el texto leído por el niño":num_palabras_leidas, "Número de aciertos":aciertos}