
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


INSERT INTO clientes (id, nombre, documento) VALUES (
    7871, 'Marin Quintero Jorge Enrique', '86053663');

INSERT INTO empresas (nombre, direccion, nit) VALUES (
    'Pollo Andino S.A.', 'Cra 27 N 36-36', '860076820-1');

INSERT INTO facturas (id, cliente_id, empresa_nit, fecha, total) VALUES (
    1, 7871, '860076820-1', '17-05-2025', 470000);

INSERT INTO items_factura (factura_id, descripción, cantidad, precio_unitario) VALUES (
    1, 'Pollo Sin Viscera De 1300 Gr Refrigerado', 16.000, 9400);

INSERT INTO items_factura (factura_id, descripción, cantidad, precio_unitario) VALUES (
    1, 'Pollo Sin Viscera De 1500 Gr Refrigerado', 34.000, 9400);