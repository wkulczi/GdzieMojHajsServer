CREATE TABLE "user" (
  "user_id" serial PRIMARY KEY,
  "login" varchar,
  "password" varchar,
  "question" varchar,
  "answer" varchar,
  "role" varchar
);
 
CREATE TABLE "receipt" (
  "receipt_id" serial PRIMARY KEY,
  "user_id" int,
  "company_id" int
);

CREATE TABLE "company" (
  "company_id" serial PRIMARY KEY,
  "category_id" int,
  "name" varchar
);

CREATE TABLE "receipt_product" (
  "receipt_id" int,
  "product_id" int,
  "quantity" int,
  PRIMARY KEY ("receipt_id", "product_id")
);

CREATE TABLE "product" (
  "product_id" serial PRIMARY KEY,
  "name" varchar,
  "price" float
);

CREATE TABLE "category" (
  "category_id" serial PRIMARY KEY,
  "pkd_code" varchar,
  "name" varchar
);

ALTER TABLE "receipt" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "receipt_product" ADD FOREIGN KEY ("receipt_id") REFERENCES "receipt" ("receipt_id");

ALTER TABLE "receipt" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("company_id");

ALTER TABLE "receipt_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");
