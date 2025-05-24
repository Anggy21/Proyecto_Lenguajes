import random

def generar_sql(datos):
    sql = []

    cliente_id = random.randint(1000, 9999)  
    factura_id = datos.get("factura_id", 1)

    # INSERT en clientes
    nombre_cliente = datos["cliente_nombre"] or 'NULL'
    documento = datos["cliente_documento"] or 'NULL'
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

    # INSERTs en items_factura
    for item in datos.get("items", []):
        cantidad_unidad = item["unidad"]
        kilos = item["kilos"] if item["kilos"] is not None else 'NULL'
        valor = item["valor"]
        descripcion = item["descripcion"]
        sql.append(f"""INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    {factura_id}, '{descripcion}', {cantidad_unidad}, {kilos}, {valor});""")

    return "\n\n".join(sql)



