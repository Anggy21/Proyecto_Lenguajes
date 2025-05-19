import pytesseract
from PIL import Image
import pytesseract
import cv2
import os
import parser


#progrma que permite leer imagenes
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\tesseract\tessdata"

imagen = cv2.imread(r'imagenes\factura.png')

# Convertir a escala de grises
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Binarizar (umbral adaptativo es mejor para fondos desiguales)
thresh = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

cv2.imwrite('preprocesada.png', thresh)

texto = pytesseract.image_to_string(thresh, lang='spa')

print("🧾 TEXTO DETECTADO:")
print(texto)

datos = parser.extraer_datos(texto)

sql_script = parser.generar_sql(datos)

with open("factura_generada.sql", "w", encoding="utf-8") as salida:
    salida.write(sql_script)

print("✅ Proceso completo: texto extraído y SQL generado.")

