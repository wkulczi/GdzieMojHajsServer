INSERT INTO uzytkownik (login, password, question, answer, role) VALUES
('test', 'test', 'Jaki jest login?', 'test', 'admin'),
('magda', 'gessler', 'Jaki jest login?', 'test', 'user');

INSERT INTO produkt (nazwa, cena) VALUES
('bagieta czosnkowa', 2.50),
('czipsy', 5.53),
('pyndzel', 5.37);

INSERT INTO kategoria (kod_pkd, nazwa_kategorii) VALUES
(1,'spozywcze'),
(2,'budowlane'),
(3,'muzyczne');

INSERT INTO firma (id_kategorii, nazwa) VALUES
(1,'biedra'),
(1,'lidl'),
(2,'leroj merlin');

INSERT INTO paragon (id_uzytkownika, id_firmy) VALUES
(1,1),
(1,2),
(2,3);

INSERT INTO paragon_produkt (id_paragonu, id_produktu, ilosc) VALUES
(1,1,2),
(1,2,5),
(3,3,2);







