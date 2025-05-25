import pdfplumber

def extraer_texto_pdf(ruta_pdf, ruta_salida=r"datos_pdf/texto_desde_pdf.txt"):
    texto_completo = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    
    # Guardar el texto en un archivo
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(texto_completo)
    
    print(f"✅ Texto extraído guardado en '{ruta_salida}'")
    return texto_completo