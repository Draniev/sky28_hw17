-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)
SELECT customers.company_name, employees.last_name FROM orders
INNER JOIN customers USING(customer_id)
INNER JOIN employees USING(employee_id)
INNER JOIN shippers ON orders.ship_via = shippers.shipper_id
WHERE customers.city = 'London' AND employees.city = 'London' 
AND shippers.company_name = 'United Package'


-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях 
-- Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.
SELECT product_name, units_in_stock, suppliers.contact_name, suppliers.phone FROM products
INNER JOIN suppliers USING(supplier_id)
INNER JOIN categories USING(category_id)
WHERE discontinued = 0 AND
categories.category_name IN ('Dairy Products', 'Condiments') AND
units_in_stock < 25
ORDER BY units_in_stock

-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа
SELECT * FROM customers
FULL JOIN orders USING(customer_id)
WHERE orders.order_id IS NULL


-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см 
--    в колонке quantity табл order_details)
--    Этот запрос написать именно с использованием подзапроса.

-- Долго думал что же именно тут надо!
SELECT SUM(quantity), products.product_name FROM order_details
INNER JOIN products USING(product_id)
GROUP BY products.product_name

SELECT DISTINCT product_name FROM products
INNER JOIN order_details USING(product_id)
WHERE order_details.quantity = 10

SELECT DISTINCT product_name FROM products
WHERE EXISTS (SELECT quantity FROM order_details WHERE order_details.product_id = products.product_id AND quantity = 10)
