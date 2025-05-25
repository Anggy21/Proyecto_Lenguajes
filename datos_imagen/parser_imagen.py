import re

def extraer_datos(texto):
    datos = {}
    errores_extraccion = {}

    with open(texto, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()

    # Cliente
    cliente = re.search(r'Sr[\W_]*\(?a\)?[\W_:]*([A-ZÁÉÍÓÚÑa-záéíóúñ ]{3,})', texto, re.IGNORECASE)
    if cliente:
        datos["cliente_nombre"] = cliente.group(1).strip().title()
    else:
        # Buscar nombres que aparezcan después de un patrón similar, aunque deformado
        posibles_nombres = re.findall(r'(?:Sr[\W_]*\(?a\)?[\W_:]*)([^\n\d]{3,40})', texto, re.IGNORECASE)
    
        if posibles_nombres:
            nombre_candidato = posibles_nombres[0].strip().title()
            datos["cliente_nombre"] = nombre_candidato
            errores_extraccion["cliente_nombre"] = f"Nombre extraído desde patrón deformado: '{nombre_candidato}'"
        else:
            datos["cliente_nombre"] = None
            # Buscar cualquier texto después de "{a):" o similar
            deformes = re.findall(r'\{?a\)?[:\-\s_]+([^\n\d]{3,40})', texto, re.IGNORECASE)
            errores_extraccion["cliente_nombre"] = (
                "No se encontró nombre con patrón esperado. "
                f"Posibles coincidencias: {deformes}"
            )

    # Documento
    doc = re.search(r'Documento\s*No[\s:]*([0-9oO]{5,})', texto, re.IGNORECASE)
    if doc:
        documento = re.sub(r'[oO]', '0', doc.group(1))
        datos["cliente_documento"] = documento
    else:
        datos["cliente_documento"] = None
        posibles_doc = re.findall(r'Documento\s*[^:\n]*\s*([^\n]+)', texto)
        errores_extraccion["cliente_documento"] = f"No se encontró documento. Posibles coincidencias: {posibles_doc}"

    # Fecha
    fecha = re.search(r'Fecha[:\s]*([0-9]{1,2})\s*([a-zA-Z]*)', texto)
    if fecha:
        dia, mes = fecha.groups()
        meses = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        mes_num = meses.get(mes.lower(), "05") if mes else "05"
        datos["fecha"] = f"2025-{mes_num}-{int(dia):02d}"
    else:
        datos["fecha"] = None
        errores_extraccion["fecha"] = "No se encontró una fecha con formato reconocible"

    # Empresa
    datos["empresa_nombre"] = "MaxiPollo"

    # Dirección
    direccion_emp = re.search(r'(Mz\s*\w+\s*casa\s*No\.\s*\d+.*?)\s*(Tel|R[eé]gimen)', texto, re.IGNORECASE)
    datos["empresa_direccion"] = direccion_emp.group(1).strip() if direccion_emp else None

    # NIT
    nit = re.search(r'\bNIT[:\s,]*([0-9,]{4,20}(?:-[a-z0-9]+)?)', texto, re.IGNORECASE)
    if nit:
        datos["empresa_nit"] = nit.group(1).strip().replace(",", "")
    else:
        # Buscar deformaciones del texto tipo "NITOG", "N1T", "NIt.", etc.
        nit_deformado = re.search(r'\bN[\W_]*[I1lT]{1}[\W_]*[0O]?G?[\W_]*[:\-]?\s*([0-9]{4,15}(?:-[a-z0-9]+)?)', texto, re.IGNORECASE)
        if nit_deformado:
            datos["empresa_nit"] = nit_deformado.group(1).strip()
            errores_extraccion["empresa_nit"] = f"NIT extraído automáticamente desde texto deformado: '{nit_deformado.group(0).strip()}'"
        else:
            # Buscar coincidencias con "NIT" al inicio de una línea
            posibles_nits = re.findall(r'\bN\w{2,6}[\s:,]*([0-9]{4,15}(?:-[a-z0-9]+)?)', texto, re.IGNORECASE)
            if posibles_nits:
                datos["empresa_nit"] = posibles_nits[0].strip()
                errores_extraccion["empresa_nit"] = f"NIT extraído desde coincidencia alternativa: '{posibles_nits[0]}'"
            else:
                datos["empresa_nit"] = None
                errores_extraccion["empresa_nit"] = "No se extrajo el NIT. Ninguna coincidencia válida encontrada."

    # Factura ID
    factura_id = re.search(r'\b(No|N[ml])[.:]?\s*(\d+)', texto, re.IGNORECASE)
    datos["factura_id"] = int(factura_id.group(2)) if factura_id else None

    # Total
    total = re.search(r'TOTAL\s*\$?\s*([0-9]+)', texto, re.IGNORECASE)
    datos["total"] = int(total.group(1)) if total else None

    # Items
    item_regex = re.findall(
        r'(Pollo|Menudencia|A(?:las|as)?|Coraz[oó]n)\s+(\d{1,5})\s+(\d{1,5})', texto, re.IGNORECASE)

    datos["items"] = []
    if item_regex:
        for descripcion, val1, val2 in item_regex:
            valor, unidad = (int(val1), int(val2)) if int(val1) > int(val2) else (int(val2), int(val1))
            datos["items"].append({
                "descripcion": descripcion.capitalize(),
                "unidad": unidad,
                "kilos": None,
                "valor": valor
            })
    else:
        errores_extraccion["items"] = "No se encontraron productos con patrón válido."

    return datos, errores_extraccion
