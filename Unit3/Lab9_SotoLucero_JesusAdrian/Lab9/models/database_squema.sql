CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL UNIQUE,
	pass VARCHAR(50) NOT NULL,
	nombre VARCHAR(100) NOT NULL
);

CREATE TABLE productos (
	id SERIAL PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	precio DECIMAL(10, 2) NOT NULL,
	stock INT NOT NULL
);

INSERT INTO users (username, pass, nombre) 
VALUES ('admin', 'admin123', 'Adrian Soto');

INSERT INTO productos (nombre, precio, stock)
VALUES 
('Laptop HP', 12500.50, 10),
('Mouse Inalambrico', 350.00, 25),
('Teclado Inalambrico', 850.00, 15);
