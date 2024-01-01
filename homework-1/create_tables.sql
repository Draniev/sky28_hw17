-- SQL-команды для создания таблиц
CREATE TABLE customers
(
	customer_id char(5) PRIMARY KEY,
	company_name varchar(255),
	contact_name varchar(255)
);

CREATE TABLE employees
(
	employee_id serial PRIMARY KEY,
	first_name varchar(255),
	last_name varchar(255),
	title varchar(255),
	birth_date date,
	notes text
);

CREATE TABLE orders
(
	order_id serial PRIMARY KEY,
	customer_id char(5) REFERENCES customers(customer_id),
	employee_id int REFERENCES employees(employee_id),
	order_date date NOT NULL,
	ship_city varchar(255)
);
