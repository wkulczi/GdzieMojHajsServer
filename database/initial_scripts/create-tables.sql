CREATE TABLE "uzytkownik" (
  "id_uzytkownika" serial PRIMARY KEY,
  "login" varchar,
  "password" varchar,
  "question" varchar,
  "answer" varchar,
  "role" varchar
);
 
CREATE TABLE "paragon" (
  "id_paragonu" serial PRIMARY KEY,
  "id_uzytkownika" int,
  "id_firmy" int
);

CREATE TABLE "firma" (
  "id_firmy" serial PRIMARY KEY,
  "id_kategorii" int,
  "nazwa" varchar
);

CREATE TABLE "paragon_produkt" (
  "id_paragonu" int,
  "id_produktu" int,
  "ilosc" int,
  PRIMARY KEY ("id_paragonu", "id_produktu")
);

CREATE TABLE "produkt" (
  "id_produktu" serial PRIMARY KEY,
  "nazwa" varchar,
  "cena" float
);

CREATE TABLE "kategoria" (
  "id_kategorii" serial PRIMARY KEY,
  "kod_pkd" varchar,
  "nazwa_kategorii" varchar
);

ALTER TABLE "paragon" ADD FOREIGN KEY ("id_uzytkownika") REFERENCES "uzytkownik" ("id_uzytkownika");

ALTER TABLE "paragon_produkt" ADD FOREIGN KEY ("id_paragonu") REFERENCES "paragon" ("id_paragonu");

ALTER TABLE "paragon" ADD FOREIGN KEY ("id_firmy") REFERENCES "firma" ("id_firmy");

ALTER TABLE "paragon_produkt" ADD FOREIGN KEY ("id_produktu") REFERENCES "produkt" ("id_produktu");
