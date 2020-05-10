CREATE TABLE "account" (
  "id" serial PRIMARY KEY,
  "login" varchar,
  "password" varchar,
  "question" varchar,
  "answer" varchar,
  "role" varchar
);
 
CREATE TABLE "receipt" (
  "id" serial PRIMARY KEY,
  "account_id" int,
  "company_id" int
);

CREATE TABLE "company" (
  "id" serial PRIMARY KEY,
  "category_id" int,
  "company_name" varchar
);

CREATE TABLE "receipt_product" (
  "receipt_id" int,
  "product_id" int,
  "quantity" int,
  PRIMARY KEY ("receipt_id", "product_id")
);

CREATE TABLE "product" (
  "id" serial PRIMARY KEY,
  "product_name" varchar,
  "price" float
);

CREATE TABLE "category" (
  "id" serial PRIMARY KEY,
  "pkd_code" varchar,
  "category_name" varchar,
  "description" varchar
);

ALTER TABLE "receipt" ADD FOREIGN KEY ("account_id") REFERENCES "account" ("id");

ALTER TABLE "receipt_product" ADD FOREIGN KEY ("receipt_id") REFERENCES "receipt" ("id");

ALTER TABLE "receipt" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("id");

ALTER TABLE "receipt_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("id");
