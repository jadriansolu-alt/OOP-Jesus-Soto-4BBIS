CREATE TABLE login_system_db.users (
	id int NOT NULL,
	username varchar NOT NULL,
	pass varchar NOT NULL,
	nombre varchar NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);

INSERT INTO users (id, nombre, pass, nombre) 
VALUES (1, 'admin', 'admin123', 'Adrian Soto');

CREATE TABLE login_system_db.productos (
	id int NOT NULL,
	nombre varchar NOT NULL,
	precio decimal NOT NULL,
	stock int NOT NULL,
	CONSTRAINT productos_pk PRIMARY KEY (id)
);

INSERT INTO productos (id, nombre, precio, stock)
VALUES (1, 'Laptop HP', 12500.50, 10),
	   (2, 'Mouse Inalambrico', 350.00, 25),
	   (3, 'Teclado Inalambrico', 850.00, );