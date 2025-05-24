import random

def generar_sql_pdf(datos):
    sql = []

    cliente_id = random.randint(1000, 9999)
    factura_id = datos.get("factura_id", 1)

    # INSERT en clientes
    nombre_cliente = datos["cliente"] or 'NULL'
    documento = datos["cedula"] or 'NULL'
    sql.append(f"""INSERT INTO clientes (id, nombre, documento) VALUES (
    {cliente_id}, '{nombre_cliente}', '{documento}');""")

    # INSERT en empresas
    empresa_nombre = datos["empresa_nombre"] or 'NULL'
    empresa_direccion = datos["empresa_direccion"] or 'NULL'
    empresa_nit = datos["empresa_nit"] or 'NULL'
    sql.append(f"""INSERT INTO empresas (nombre, direccion, nit) VALUES (
    '{empresa_nombre}', '{empresa_direccion}', '{empresa_nit}');""")

    # INSERT en facturas
    fecha = datos["fecha"] or '2025-01-01'
    total = datos["total"] or 0
    sql.append(f"""INSERT INTO facturas (id, cliente_id, empresa_nit, fecha, total) VALUES (
    {factura_id}, {cliente_id}, '{empresa_nit}', '{fecha}', {total});""")

    # INSERTs en items_factura (corregido)
    for item in datos.get("items", []):
        cantidad = item["cantidad"]
        precio_unitario = item["precio_unitario"]
        descripcion = item["descripcion"]
        sql.append(f"""INSERT INTO items_factura (factura_id, descripción, cantidad, precio_unitario) VALUES (
    {factura_id}, '{descripcion}', {cantidad}, {precio_unitario});""")

    return "\n\n".join(sql)
