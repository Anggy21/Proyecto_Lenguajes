import streamlit as st
import os
import tempfile

from datos_imagen.ocr import process_file as ocr_process_file
from datos_pdf.extraer_pdf import extraer_texto_pdf
from datos_imagen.parser_imagen import extraer_datos as extraer_datos_imagen
from datos_imagen.generar_sql_imagen import generar_sql as generar_sql_imagen
from datos_pdf.parser_pdf import extraer_datos_pdf
from datos_pdf.sql_pdf import generar_sql_pdf

st.set_page_config(page_title="Generador de SQL desde Facturas", layout="centered")

st.title("🧾 Generador de SQL desde Facturas")
st.write("Sube un archivo de factura (imagen o PDF) y genera automáticamente el script SQL.")

archivo = st.file_uploader("📂 Sube tu archivo (.png, .jpg o .pdf)", type=["png", "jpg", "pdf"])

if archivo:
    extension = os.path.splitext(archivo.name)[1].lower()

    # Vista previa
    st.subheader("Vista previa del archivo")
    if extension in [".png", ".jpg"]:
        st.image(archivo, use_column_width=True)
    elif extension == ".pdf":
        st.write("📄 Archivo PDF subido.")

    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        tmp.write(archivo.read())
        tmp_path = tmp.name

    errores = {}
    datos = None
    sql_script = ""

    # Procesamiento según tipo
    if extension in [".png", ".jpg"]:
        st.info("🖼 Procesando imagen...")
        ocr_process_file(tmp_path)
        ruta_texto = r"datos_imagen\resultado_corregido.txt"
        datos, errores = extraer_datos_imagen(ruta_texto)
        sql_script = generar_sql_imagen(datos)
    else:
        st.info("📄 Procesando PDF...")
        texto = extraer_texto_pdf(tmp_path)
        ruta_texto = r"datos_pdf\texto_desde_pdf.txt"
        datos, errores = extraer_datos_pdf(ruta_texto)
        sql_script = generar_sql_pdf(datos)

    # Guardar SQL generado
    ruta_sql = "factura_generada.sql"
    with open(ruta_sql, "w", encoding="utf-8") as f:
        f.write(sql_script)

    # Mostrar SQL generado
    st.subheader("📜 Script SQL generado")
    st.code(sql_script, language="sql")

    # Descargar SQL
    with open(ruta_sql, "rb") as f:
        st.download_button(
            label="📥 Descargar factura_generada.sql",
            data=f,
            file_name="factura_generada.sql",
            mime="text/sql"
        )

    # Mostrar errores si los hay
    if errores:
        st.subheader("⚠ Errores detectados en la extracción")
        for campo, mensaje in errores.items():
            st.warning(f"{campo.upper()}: {mensaje}")
