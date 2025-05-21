import parser
import ocr


datos = parser.extraer_datos(ocr.texto)

sql_script = parser.generar_sql(datos)

with open("factura_generada.sql", "w", encoding="utf-8") as salida:
    salida.write(sql_script)

print("✅ Proceso completo: texto extraído y SQL generado.")

