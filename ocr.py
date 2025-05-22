import os
import easyocr
import cv2
import numpy as np
import pdfplumber

def read_image_with_easyocr(img_path):
    reader = easyocr.Reader(['es'])
    img = cv2.imread(img_path)
    if img is None:
        print(f"No se pudo cargar la imagen: {img_path}")
        return
    result = reader.readtext(img)
    print(f"Texto extraído de la imagen '{img_path}':")
    for bbox, text, prob in result:
        print(f"  Texto: {text}, Confianza: {prob:.2f}")

def read_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Texto extraído del PDF '{pdf_path}':")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"\n--- Página {i + 1} ---\n")
            print(text if text else "[Página vacía o no extraíble]")

def main(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        read_image_with_easyocr(file_path)
    elif ext == '.pdf':
        read_pdf_text(file_path)
    else:
        print(f"Extensión '{ext}' no soportada.")

if __name__ == "__main__":
    file_path = "archivos/stiven.jpg"  # Cambia esto al archivo que quieras probar
    main(file_path)
