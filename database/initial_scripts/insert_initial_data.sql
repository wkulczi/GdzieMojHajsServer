INSERT INTO "user" (login, password, question, answer, role) VALUES
('test', 'test', 'Jaki jest login?', 'test', 'admin'),
('magda', 'gessler', 'Jaki jest login?', 'test', 'user');

INSERT INTO product (name, price) VALUES
('bagieta czosnkowa', 2.50),
('czipsy', 5.53),
('pyndzel', 5.37);

INSERT INTO category (pkd_code, name) VALUES
(1,'spozywcze'),
(2,'budowlane'),
(3,'muzyczne');

INSERT INTO company (category_id, name) VALUES
(1,'Warzywniak'),
(1,'Spozywczak'),
(2,'leroj merlin');

INSERT INTO receipt (user_id, company_id) VALUES
(1,1),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(1,2),
(2,3);

INSERT INTO receipt_product (receipt_id, product_id, quantity) VALUES
(1,1,2),
(1,2,5),
(2,3,2),
(3,3,2),
(4,3,2),
(5,3,2),
(6,3,2),
(7,3,2),
(8,3,2),
(9,3,2),
(10,3,2),
(11,3,2),
(12,3,2),
(13,3,2);







