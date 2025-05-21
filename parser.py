import re
import random

def extraer_datos(texto):
    datos = {}

    # Empresa
    lineas = [linea.strip() for linea in texto.strip().split('\n') if linea.strip()]
    if len(lineas) >= 2:
        datos['empresa'] = lineas[0]
        datos['direccion_empresa'] = lineas[1]
    else:
        datos['empresa'] = 'EMPRESA_DESCONOCIDA'
        datos['direccion_empresa'] = 'DIRECCION_DESCONOCIDA'

    # Cliente
    match_cliente = re.search(r'Enviara\s+([a-záéíóúüñ\s]+)', texto, re.IGNORECASE)
    if match_cliente:
        datos['cliente'] = match_cliente.group(1).strip().title()
    else:
        datos['cliente'] = 'CLIENTE_DESCONOCIDO'

    
    match_direccion = re.search(r'(virgen blanca[^\n]+)', texto, re.IGNORECASE)
    if match_direccion:
        datos['direccion_cliente'] = match_direccion.group(1).strip()
    else:
        datos['direccion_cliente'] = 'DIRECCION_DESCONOCIDA'



    # Número y fecha de factura
    match_factura = re.search(r'n[°º*]?\s*(de\s+factura)?\s*(ES-\d+)', texto, re.IGNORECASE)
    if match_factura:
        datos['factura_id'] = match_factura.group(2)
    else:
        datos['factura_id'] = 'SIN_NUMERO'

    # Fecha
    match_fecha = re.search(r'fecha\s*[—\-]?\s*(\d{8})', texto, re.IGNORECASE)
    if match_fecha:
        fecha_str = match_fecha.group(1)
        datos['fecha'] = f"{fecha_str[4:8]}-{fecha_str[2:4]}-{fecha_str[0:2]}"
    else:
        datos['fecha'] = '0000-00-00'


 

    # Ítems
    datos['items'] = []
    item_patron = re.compile(r'(\d+)\s*\|\s*(.*?)\s+([\d,]+)\s+([\d,]+)', re.MULTILINE)
    for cantidad, descripcion, precio, importe in item_patron.findall(texto):
        datos['items'].append({
            'cantidad': int(cantidad),
            'descripcion': descripcion.strip(),
            'precio_unitario': float(precio.replace(',', '.')),
            'importe': float(importe.replace(',', '.'))
        })

    # Totales
    match_subtotal = re.search(r'subt[o0]l[aá]l?\s*([\d.,]+)', texto, re.IGNORECASE)
    if match_subtotal:
        datos['subtotal'] = float(match_subtotal.group(1).replace(',', '.'))
    else:
        datos['subtotal'] = 0.0
        print("⚠️ No se encontró el subtotal en el texto OCR.")

    match_iva = re.search(r'iva\s*\d{1,2}[.,]?\d*%?\s*([\d.,]+)', texto, re.IGNORECASE)
    if not match_iva:
        match_iva = re.search(r'iva\d{1,2}[.,]?\d*%?\s*([\d.,]+)', texto, re.IGNORECASE)

    if match_iva:
        datos['iva'] = float(match_iva.group(1).replace(',', '.'))
    else:
        datos['iva'] = 0.0
        print("⚠️ No se encontró el IVA en el texto OCR.")


    datos['total'] = float(re.search(r'TOTAL\s+([\d,]+)', texto).group(1).replace(',', '.'))

    return datos


def formatear_fecha(fecha_str):
    if not fecha_str:
        return "0000-00-00"
    fecha_str = fecha_str.strip().replace('/', '').replace('-', '')
    if len(fecha_str) == 8 and fecha_str.isdigit():
        dia = fecha_str[0:2]
        mes = fecha_str[2:4]
        anio = fecha_str[4:]
        return f"{anio}-{mes}-{dia}"
    return "0000-00-00"


def generar_sql(datos):
    sql = []

    factura_id = datos.get('factura_id', 'SIN_NUMERO')
    cliente_id = datos.get('cliente_id', f"CL-{random.randint(1000,9999)}")

    # Insertar cliente
    sql.append(f"""INSERT INTO clientes (cliente_id, nombre, direccion) 
VALUES ('{cliente_id}', '{datos['cliente']}', '{datos['direccion_cliente']}');""")

    # Insertar factura
    sql.append(f"""INSERT INTO facturas (factura_id, empresa, direccion_empresa, cliente_id, fecha, subtotal, iva, total) 
VALUES ('{factura_id}', '{datos['empresa']}', '{datos['direccion_empresa']}', '{cliente_id}', 
'{formatear_fecha(datos['fecha'])}', {datos['subtotal']}, {datos['iva']}, {datos['total']});""")

    # Insertar ítems
    for item in datos['items']:
        sql.append(f"""INSERT INTO items_factura (factura_id, cantidad, descripcion, precio_unitario, importe) VALUES 
('{factura_id}', {item['cantidad']}, '{item['descripcion']}', {item['precio_unitario']}, {item['importe']});""")

    return '\n'.join(sql)



# Solo ejecuta si este archivo se llama directamente
if __name__ == '__main__':
    with open("texto_extraido.txt", "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    datos = extraer_datos(texto)
    sql_script = generar_sql(datos)

    with open("factura_generada.sql", "w", encoding="utf-8") as salida:
        salida.write(sql_script)

    print("✅ Script SQL generado con éxito en 'factura_generada.sql'")
