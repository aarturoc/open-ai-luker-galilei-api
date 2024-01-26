import string
import unidecode

def CompareFromText(texto_niño):

    texto_guia = """María tiene una gata. A la gata le gusta jugar. Un día María no encontró a su gata. María y su mamá la buscaron por toda la casa. De pronto oyeron “miau, miau”. Los maullidos eran suaves. Venían de debajo de la cama. María y su mamá encontraron a la gata y dos gatitos. La gata de María tuvo gatitos. La mamá de María le dijo: Yo también tendré un bebé. Vas a tener un hermanito. María sonrió y se fue corriendo a la casa de su amiga Lorena. Al llegar le dijo a Lorena: “Vengo a contarte grandes noticias"""
    # Crear una tabla de traducción para eliminar puntuaciones, tildes y caracteres especiales
    translator = str.maketrans("", "", string.punctuation)

    # Eliminar tildes y diacríticos utilizando la biblioteca unidecode
    texto_guia = unidecode.unidecode(texto_guia)
    texto_niño = unidecode.unidecode(texto_niño)

    # Tokenizar el texto en palabras, eliminar puntuaciones y convertir a minúsculas
    palabras_guia = [palabra.translate(translator) for palabra in texto_guia.lower().split()]
    palabras_niño = [palabra.translate(translator) for palabra in texto_niño.lower().split()]

    # Crear un diccionario para contar la frecuencia de cada palabra en el texto guía
    dic_guia = {}
    for palabra in palabras_guia:
        dic_guia[palabra] = dic_guia.get(palabra, 0) + 1

    # Crear un diccionario para contar la frecuencia de cada palabra en el texto del niño
    dic_niño = {key: 0 for key in dic_guia}

    # Contar la frecuencia de cada palabra en el texto del niño
    for palabra_niño in palabras_niño:
        if palabra_niño in dic_guia:
            dic_niño[palabra_niño] += 1


    palabras_totales=len(palabras_guia)
    palabras_leidas=len(palabras_niño)
    diferencia_total = palabras_totales-sum(abs(dic_guia[llave] - dic_niño[llave]) for llave in dic_guia)

    return {"Total palabras":palabras_totales, "Palabras leídas": palabras_leidas, "Aciertos": diferencia_total}