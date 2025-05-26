import cv2
import torch
from easyocr import Reader
import difflib
import unicodedata
import re

# Diccionario básico ampliado con las palabras correctas conocidas
diccionario = [
    "cantidad", "código", "descripción", "precios", "valor", "unidad", "kilos",
    "factura", "para", "sus", "oficios", "legales", "un", "título",
    "según", "ley", "de", "julio", "menudencia", "stiven", "villarraga","Loy",
    "corazón", "alas","Pollo", "pollo", "Corazón", "alas", "Corazón",
    "al", "mayor", "mayo", "detalle", "ventas","Régimen","Anggy" ,"Michelle","Firma","sus","Alfonso" # <-- Agregué "mayo"
]


# Diccionario para reemplazos directos por palabras específicas mal reconocidas
reemplazos_automaticos = {
    "henvlencici": "menudencia",
    "henvencici": "menudencia",
    "shvea": "stiven",
    "ifaga": "villarraga",
    "cora2sn": "corazón",
    "ala5": "alas",
    "proclos":"Precios",
    "proclo": "precio",
    "meraencic": "Menudencia",
    "contadoc": "Contado",
    "hachelle":"Michelle",
    "hajo":"Mayo",
    "hxcheile":"Michelle",
    "p21q":"Pollo",
    "catazzn":"Corazón",
    "shwvea":"Stiven",
    "ulla":"Villarraga",
    "shuven":"Stiven",
    "eus":"sus",
    "pole":"Pollo",
    "pøll":"Pollo",
    "poll":"Pollo",
    "corazón 2on":"Corazón",
    "alas 2on":"alas",
    
}
def corregir_errores_ocr_en_numeros(texto):
    if not texto:
        return texto

    texto_corregido = texto

    # Mapa de sustitución para caracteres mal reconocidos en números
    reemplazos = {
        'c': '0', 'C': '0',
        'o': '0', 'O': '0',
        'l': '1', 'i': '1', 'I': '1',
        'q': '9', 'Q': '9',
        's': '5', 'S': '5',
        'b': '6', 'B': '6',
    }

    # Solo aplicar si hay mezcla de dígitos y letras (probable número mal leído)
    if any(ch.isdigit() for ch in texto) and any(ch.isalpha() for ch in texto):
        texto_corregido = ''.join(reemplazos.get(ch, ch) for ch in texto)

        # Validación opcional: si tras corregir es un número válido, lo devolvemos
        try:
            float(texto_corregido.replace(',', '.'))  # Por si usan coma como decimal
            return texto_corregido
        except ValueError:
            return texto  # Si no es un número válido, lo dejamos igual
    return texto


def corregir_nueves_como_ceros(palabra, confianza):
    if confianza < 0.5 and palabra.replace('.', '', 1).isdigit():
        # Reemplazamos 9 por 0 solo si parece un número decimal o entero
        return palabra.replace('9', '0')
    return palabra


def corregir_ceros_en_numeros(palabra):
    num_digitos = sum(ch.isdigit() for ch in palabra)
    num_letras = sum(ch.isalpha() for ch in palabra)

    # Si la palabra tiene más dígitos que letras, o sólo tiene letras 'c'/'C' confundidas,
    # entonces reemplazamos las 'c' o 'C' por '0'
    if num_digitos >= num_letras:
        palabra = palabra.replace('c', '0').replace('C', '0')
    return palabra

def conservar_formato_original(palabra_original, palabra_corregida):
    # Si original era capitalizada (ejemplo: Mayo)
    if palabra_original[0].isupper() and palabra_original[1:].islower():
        return palabra_corregida.capitalize()
    # Si original era todo mayúsculas (ejemplo: MAYO)
    elif palabra_original.isupper():
        return palabra_corregida.upper()
    # Si original todo minúsculas
    else:
        return palabra_corregida.lower()

meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.lower()


def corregir_palabra(palabra, diccionario):

    palabra_lower = palabra.lower()

    palabra_normalizada = normalizar_texto(palabra)
    if palabra_normalizada in reemplazos_automaticos:
        return conservar_formato_original(palabra, reemplazos_automaticos[palabra_normalizada])


    # Corregir ceros en números
    palabra_corr = corregir_ceros_en_numeros(palabra)

    # Excepción: corregir meses antes que nada
    matches_meses = difflib.get_close_matches(palabra_corr.lower(), meses, n=1, cutoff=0.7)
    if matches_meses:
        return conservar_formato_original(palabra, matches_meses[0])

    if len(palabra_lower) <= 3 and palabra_lower not in diccionario:
        return palabra

    matches = difflib.get_close_matches(palabra_corr.lower(), diccionario, n=1, cutoff=0.7)
    if matches:
        return conservar_formato_original(palabra, matches[0])
    else:
        return palabra



def get_easyocr_reader():
    print("[INFO] Inicializando EasyOCR...")
    lang_list = ['es', 'en']
    return Reader(lang_list, gpu=torch.cuda.is_available())

def es_espacio(v):
    return v.strip() == ""

def unir_numeros_con_punto(texto):
    """
    Recibe un texto que puede contener números separados por espacios y un punto,
    como '8 .900' o '1 . 234', y devuelve el texto con esos números unidos sin el punto,
    es decir, '8900' o '1234'.
    """
    patron = re.compile(r'(\d+)\s*\.\s*(\d+)')
    while patron.search(texto):
        texto = patron.sub(lambda m: m.group(1) + m.group(2), texto)
    return texto

def corregir_guion_a_punto_en_numero(texto, confianza, umbral=0.5):
    """
    Si la confianza es baja (menor a umbral) y el texto contiene un guion entre números,
    lo reemplaza por punto para corregir posibles errores de OCR.
    Solo se aplica si el texto es un número o número con guion en medio.
    Ejemplo: '10-592' -> '10.592'
    """
    if confianza < umbral:
        # Solo corregir si texto tiene guion y está rodeado por dígitos
        if re.match(r'^\d+-\d+$', texto):
            texto_corregido = texto.replace('-', '.')
            return texto_corregido
    return texto

def ocr_from_image(img_path):
    print(f"[DEBUG] Intentando cargar imagen: {img_path}")
    img = cv2.imread(img_path)

    if img is None:
        print(f"[ERROR] No se pudo cargar la imagen: {img_path}")
        return []

    print("[DEBUG] Imagen cargada correctamente con OpenCV. Pasando a EasyOCR...")

    h, w = img.shape[:2]
    print(f"[DEBUG] Tamaño de imagen: {w}x{h}")
    if h < 100 or w < 100:
        print("[DEBUG] Imagen muy pequeña. Redimensionando.")
        img = cv2.resize(img, (w * 2, h * 2))

    reader = get_easyocr_reader()

    try:
        result = reader.readtext(img, detail=1, min_size=10)
        print("[INFO] Resultados de OCR:")
        palabras_corregidas = []

        for bbox, text, prob in result:
            print(f"Texto original: '{text}', Confianza: {prob:.2f}")

            text = corregir_guion_a_punto_en_numero(text, prob, umbral=0.5)

            palabras = text.split()
            palabras_corr = []

            for p in palabras:
                p_corregido = corregir_palabra(p, diccionario)
                p_final = corregir_errores_ocr_en_numeros(corregir_nueves_como_ceros(p_corregido, prob))
                palabras_corr.append(p_final)

            palabras_unidas = []
            i = 0

            while i < len(palabras_corr):
                actual = palabras_corr[i]

                if actual.isdigit():
                    j = i + 1

                    # Saltar espacios después del número
                    while j < len(palabras_corr) and es_espacio(palabras_corr[j]):
                        j += 1

                    # Buscar punto
                    if j < len(palabras_corr) and palabras_corr[j] == ".":
                        j += 1
                        while j < len(palabras_corr) and es_espacio(palabras_corr[j]):
                            j += 1

                        # Si hay número después del punto
                        if j < len(palabras_corr) and palabras_corr[j].isdigit():
                            numero_unido = actual + palabras_corr[j]
                            palabras_unidas.append(numero_unido)
                            i = j + 1
                            continue

                    # Si no hubo punto, unir números consecutivos
                    numero_completo = actual
                    while j < len(palabras_corr) and palabras_corr[j].isdigit():
                        numero_completo += palabras_corr[j]
                        j += 1
                    palabras_unidas.append(numero_completo)
                    i = j
                else:
                    if not es_espacio(actual):
                        palabras_unidas.append(actual)
                    i += 1

            texto_corregido = " ".join(palabras_unidas)

            # Aquí aplicamos la limpieza que une números con punto separados por espacios
            texto_corregido = unir_numeros_con_punto(texto_corregido)

            palabras_corregidas.append(texto_corregido)

        return palabras_corregidas

    except Exception as e:
        print(f"[ERROR] Falló EasyOCR con la imagen: {img_path}")
        print(e)
        return []


def process_file(file_path):
    print(f"[INFO] Procesando archivo: {file_path}")
    resultados_corregidos = ocr_from_image(file_path)

    if resultados_corregidos:
        with open(r"datos_imagen\resultado_corregido.txt", "w", encoding="utf-8") as f:
            for linea in resultados_corregidos:
                f.write(linea + "\n")
        print(f"[INFO] Resultados corregidos guardados en", r'datos_imagen\resultado_corregido.txt')
    else:
        print("[WARN] No se obtuvieron resultados para guardar.")
        

if __name__ == "__main__":
    archivo_entrada = 'archivos/original.jpg'  # Cambia a tu imagen
    process_file(archivo_entrada)
