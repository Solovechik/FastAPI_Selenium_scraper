CREATE TABLE IF NOT EXISTS goods_to_monitor(
	id serial PRIMARY KEY
	,title VARCHAR(500) NOT NULL UNIQUE
	,description TEXT NOT NULL
	,price DECIMAL(10, 2) NULL
	,rating FLOAT NULL
	,link VARCHAR(500) NOT NULL
	);
  
  
CREATE TABLE IF NOT EXISTS price_history(
	id serial PRIMARY KEY
	,good_id INT REFERENCES goods_to_monitor(id) ON DELETE SET NULL (good_id)
	,price DECIMAL(10, 2) NOT NULL
	,added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	

CREATE OR REPLACE FUNCTION price_history_insert_func()
RETURNS TRIGGER AS
$$
BEGIN
INSERT INTO price_history(good_id, price)
VALUES(new.id, new.price);
RETURN new;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER price_history_trigger
AFTER UPDATE
ON goods_to_monitor
FOR EACH ROW
EXECUTE procedure price_history_insert_func();
