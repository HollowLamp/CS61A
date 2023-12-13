.read data.sql


CREATE TABLE average_prices AS
  SELECT category, SUM(MSRP)/COUNT(*) AS average_price FROM products
  GROUP BY category;


CREATE TABLE lowest_prices AS
  SELECT store, item, MIN(price) FROM inventory
  GROUP BY item;

CREATE TABLE item_list AS
  SELECT name as best_item, min(MSRP / rating) FROM products
  GROUP BY category;

CREATE TABLE shopping_list AS
  SELECT best_item, store FROM item_list, lowest_prices
  where best_item = item ;


CREATE TABLE total_bandwidth AS
  SELECT SUM(b.Mbs) FROM shopping_list as a, stores as b
  WHERE a.store = b.store;

