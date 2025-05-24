import re

ruta_texto = r"datos_pdf/texto_desde_pdf.txt"

def extraer_datos_pdf(texto):
    datos = {
        "cliente": {},
        "empresa": {},
        "factura": {},
        "items": []
    }
    errores_extraccion = {}

    with open(texto, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()

    # =================== EMPRESA =====================
    nit = re.search(r'Factura generada.*?Nit\s+([0-9.\-]+)', texto)
    nombre_empresa = re.search(r'^([A-Z ]+ S\.A\.)', texto, re.MULTILINE)

    if nit:
        datos["empresa"]["nit"] = nit.group(1)
    else:
        errores_extraccion["empresa_nit"] = "No se encontró el NIT."

    if nombre_empresa:
        datos["empresa"]["nombre"] = nombre_empresa.group(1).title()
    else:
        errores_extraccion["empresa_nombre"] = "No se encontró el nombre de la empresa."

    direccion_empresa = re.search(r'Cra\s+\d+\s+N\s+\d+-\d+', texto)
    if direccion_empresa:
        datos["empresa"]["direccion"] = direccion_empresa.group()
    else:
        errores_extraccion["empresa_direccion"] = "No se encontró la dirección de la empresa."

    # =================== CLIENTE =====================
    cliente = re.search(r'Cliente:\s*(.*?)\s+Medio de pago', texto)
    cedula = re.search(r'Cedula de\s+(\d+)', texto)
    direccion = re.search(r'Dirección:\s*(.*?)\s+\d', texto)
    ciudad = re.search(r'Ciudad:\s*([A-Za-z ]+)', texto)
    telefono = re.search(r'Teléfono:\s*(\d+)', texto)
    codigo = re.search(r'Código:\s*(\d+)', texto)

    if cliente:
        datos["cliente"]["nombre"] = cliente.group(1).strip().title()
    else:
        errores_extraccion["cliente_nombre"] = "No se encontró el nombre del cliente."

    datos["cliente"]["cedula"] = cedula.group(1) if cedula else None
    datos["cliente"]["direccion"] = direccion.group(1).strip() if direccion else None
    datos["cliente"]["ciudad"] = ciudad.group(1).strip().title() if ciudad else None
    datos["cliente"]["telefono"] = telefono.group(1) if telefono else None
    datos["cliente"]["codigo"] = codigo.group(1) if codigo else None

    # =================== FACTURA =====================
    factura_numero = re.search(r'Número:\s*BB\s*(\d+)', texto)
    fecha = re.search(r'Fecha\s+(\d{2}/\d{2}/\d{4})', texto)
    total = re.search(r'Total\s*\$([0-9.,]+)', texto, re.IGNORECASE)

    if factura_numero:
        datos["factura"]["numero"] = factura_numero.group(1)
    else:
        errores_extraccion["factura_numero"] = "No se encontró el número de la factura."

    datos["factura"]["cliente_id"] = datos["cliente"].get("codigo")
    datos["factura"]["empresa_nit"] = datos["empresa"].get("nit")
    datos["factura"]["fecha"] = fecha.group(1).replace('/', '-') if fecha else None
    datos["factura"]["total"] = total.group(1).replace(',', '') if total else None

    # =================== ITEMS =====================
    items = re.findall(
        r'(\d{4})\s+([A-Z\s\d]+?)\s+(\d{2})\s+KL\s+([\d.,]+)\s+\$\s*([\d.,]+)\s+\$\s*([\d.,]+)\s+\$\s*([\d.,]+)\s+([\d.,]+)',
        texto
    )
    if items:
        for item in items:
            datos["items"].append({
                "factura_id": datos["factura"].get("numero"),
                "item_codigo": item[0],
                "descripcion": item[1].strip().title(),
                "cantidad": item[3].replace(',', '.'),
                "precio_unitario": item[4].replace(',', ''),
                "valor_total": item[6].replace(',', ''),
                "iva": item[7].replace(',', '.')
            })
    else:
        errores_extraccion["items"] = "No se encontraron ítems de factura."

    return datos, errores_extraccion

# Ejecución
datos, errores = extraer_datos_pdf(ruta_texto)

print("DATOS EXTRAIDOS:")
for k, v in datos.items():
    print(f"{k}: {v}")

print("\nERRORES DE EXTRACCIÓN:")
for k, v in errores.items():
    print(f"{k}: {v}")
