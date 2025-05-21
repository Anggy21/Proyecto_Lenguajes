import pytesseract
from PIL import Image
import pytesseract
import cv2
import os
import fitz


#progrma que permite leer imagenes
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\tesseract\tessdata"

ruta_imagen = cv2.imread(r'archivos\grises.jpg')
ruta_pdf = r"archivos\facturaSavicol.pdf"



def extraer_texto_pdf_embebido(ruta_pdf):
    # Abrir el archivo PDF
    documento = fitz.open(ruta_pdf)
    texto_total = ""

    # Recorrer cada página
    for i, pagina in enumerate(documento):
        texto = pagina.get_text()
        texto_total += f"\n--- Página {i+1} ---\n{texto}"

    documento.close()
    return texto_total


#texto = extraer_texto_pdf_embebido(ruta_pdf)
texto = pytesseract.image_to_string(ruta_imagen, lang='spa')

print("🧾 TEXTO DETECTADO:")
print(texto)