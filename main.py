from datos_imagen.parser_imagen import extraer_datos
from datos_imagen.generar_sql_imagen import generar_sql
from datos_pdf.parser_pdf import extraer_datos_pdf
from datos_pdf.sql_pdf import generar_sql_pdf

def main():
    ruta_imagen = r"datos_imagen\resultado_corregido.txt"
    ruta_texto = r"datos_pdf\texto_desde_pdf.txt"

    # Ejecutar el parser
    datos, errores = extraer_datos_pdf(ruta_texto)

    # Generar el SQL
    sql_script = generar_sql_pdf(datos)

    # Guardar el archivo SQL
    with open(r"datos_pdf/factura_generada.sql", "w", encoding="utf-8") as salida:
        salida.write(sql_script)

    print("✅ Script SQL generado con éxito en 'factura_generada.sql'")

    # Mostrar errores si los hay
    if errores:
        with open(r"datos_imagen/errores_extraccion.log", "w", encoding="utf-8") as log:
            for campo, mensaje in errores.items():
                log.write(f"{campo.upper()}: {mensaje}\n")
        print(f"⚠ Algunos errores fueron registrados en", 'datos_imagen/errores_extraccion.log')

if __name__ == "__main__":
    main()
