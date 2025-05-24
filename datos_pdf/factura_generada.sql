INSERT INTO clientes (id, nombre, documento) VALUES (
    7604, 'Stiven', '106868866');

INSERT INTO empresas (nombre, direccion, nit) VALUES (
    '?Isoudota', 'Mz 2H casa No. 2 Salitre', '86053663-3');

INSERT INTO facturas (id, cliente_id, empresa_nit, fecha, total) VALUES (
    6484, 7604, '86053663-3', '2025-05-20', 1153012);

INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    6484, 'Pollo', 2, NULL, 45200);

INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    6484, 'Menudencia', 5, NULL, 10502);

INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    6484, 'Alas', 10, NULL, 5030);

INSERT INTO items_factura (factura_id, descripción, cantidad_unidad, cantidad_kilos, valor) VALUES (
    6484, 'Corazón', 2, NULL, 8900);