import random

def generar_sql_pdf(datos):
    sql = []

    cliente_id = random.randint(1000, 9999)
    factura_id = datos.get("factura", {}).get("numero", 1)

    # ===================== CREAR TABLAS =====================
    sql.append("""
-- ===================== TABLAS =====================

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
    cantidad DECIMAL(10,2),
    precio_unitario DECIMAL(12,2),
    FOREIGN KEY (factura_id) REFERENCES facturas(id)
);
""")

    # ===================== INSERTS =====================

    # CLIENTES
    nombre_cliente = datos.get("cliente", {}).get("nombre", 'NULL')
    documento = datos.get("cliente", {}).get("documento", 'NULL')
    sql.append(f"""INSERT INTO clientes (id, nombre, documento) VALUES (
    {cliente_id}, '{nombre_cliente}', '{documento}');""")

    # EMPRESAS
    empresa_nombre = datos.get("empresa", {}).get("nombre", 'NULL')
    empresa_direccion = datos.get("empresa", {}).get("direccion", 'NULL')
    empresa_nit = datos.get("empresa", {}).get("nit", 'NULL')
    sql.append(f"""INSERT INTO empresas (nombre, direccion, nit) VALUES (
    '{empresa_nombre}', '{empresa_direccion}', '{empresa_nit}');""")

    # FACTURAS
    fecha = datos.get("factura", {}).get("fecha", '2025-01-01')
    total = datos.get("factura", {}).get("total", 0)
    sql.append(f"""INSERT INTO facturas (id, cliente_id, empresa_nit, fecha, total) VALUES (
    {factura_id}, {cliente_id}, '{empresa_nit}', '{fecha}', {total});""")

    # ITEMS
    for item in datos.get("items", []):
        descripcion = item.get("descripcion", 'NULL')
        cantidad = item.get("cantidad", 0)
        precio_unitario = item.get("precio_unitario", 0)
        sql.append(f"""INSERT INTO items_factura (factura_id, descripción, cantidad, precio_unitario) VALUES (
    {factura_id}, '{descripcion}', {cantidad}, {precio_unitario});""")

    return "\n\n".join(sql)
