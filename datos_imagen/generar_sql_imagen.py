import random

def generar_sql(datos):
    sql = []

    cliente_id = random.randint(1000, 9999)
    factura_id = datos.get("factura_id", 1)

    # ===================== CREAR TABLAS =====================
    sql.append("""

CREATE TABLE IF NOT EXISTS clientes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    documento VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS empresas (
    nit VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS facturas (
    id INT PRIMARY KEY,
    cliente_id INT,
    empresa_nit VARCHAR(20),
    fecha DATE,
    total DECIMAL(12,2),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empresa_nit) REFERENCES empresas(nit)
);

CREATE TABLE IF NOT EXISTS items_factura (
    id SERIAL PRIMARY KEY,
    factura_id INT,
    descripción VARCHAR(255),
    cantidad_unidad INT,
    cantidad_kilos DECIMAL(10,2),
    valor DECIMAL(12,2),
    FOREIGN KEY (factura_id) REFERENCES facturas(id)
);
""")

    # ===================== INSERTS =====================

    # INSERT en clientes
    nombre_cliente = datos.get("cliente_nombre", "NULL")
    documento = datos.get("cliente_documento", "NULL")
    sql.append(f"""INSERT INTO clientes (id, nombre, documento) VALUES (
    {cliente_id}, '{nombre_cliente}', '{documento}');""")

    # INSERT en empresas
    empresa_nombre = datos.get("empresa_nombre", "NULL")
    empresa_direccion = datos.get("empresa_direccion", "NULL")
    empresa_nit = datos.get("empresa_nit", "NULL")
    sql.append(f"""INSERT INTO empresas (nombre, direccion, nit) VALUES (
    '{empresa_nombre}', '{empresa_direccion}', '{empresa_nit}');""")

    # INSERT en facturas
    fecha = datos.get("fecha", "2025-01-01")
    total = datos.get("total", 0)
    sql.append(f"""INSERT INTO facturas (id, cliente_id, empresa_nit, fecha, total) VALUES (
    {factura_id}, {cliente_id}, '{empresa_nit}', '{fecha}', {total});""")

    # INSERT en items_factura
    for item in datos.get("items", []):
        cantidad_unidad = item.get("unidad", 1)
        kilos = item.get("kilos", "NULL")
        valor = item.get("valor", 0)
        descripcion = item.get("descripcion", "Sin descripción")

        sql.append(f"""INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    {factura_id}, '{descripcion}', {cantidad_unidad}, {kilos}, {valor});""")

    return "\n\n".join(sql)
