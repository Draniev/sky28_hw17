-- 1. Создать таблицу student с полями student_id serial, first_name varchar, last_name varchar, birthday date, phone varchar
CREATE TABLE student (
	student_id serial PRIMARY KEY,
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	birthday DATE,
	phone VARCHAR(255)
);

-- 2. Добавить в таблицу student колонку middle_name varchar
ALTER TABLE student ADD 
	middle_name VARCHAR(255);

-- 3. Удалить колонку middle_name
ALTER TABLE student 
	DROP COLUMN middle_name;

-- 4. Переименовать колонку birthday в birth_date
ALTER TABLE student 
	RENAME birthday TO birth_date;

-- 5. Изменить тип данных колонки phone на varchar(32)
ALTER TABLE student 
	ALTER COLUMN phone SET DATA TYPE varchar(32);

-- 6. Вставить три любых записи с автогенерацией идентификатора
INSERT INTO student (first_name, last_name, birth_date, phone) VALUES 
	('name1', 'lastname1', '1990-01-01', '+7911-111-11-11'),
	('name1', 'lastname1', '1990-01-01', '+7911-111-11-11'),
	('name1', 'lastname1', '1990-01-01', '+7911-111-11-11');	

-- 7. Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
TRUNCATE TABLE student;
