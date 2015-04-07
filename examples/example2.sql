DROP TABLE product_with_date;

CREATE TABLE product_with_date (
    name character varying(100),
    category character varying(100),
    price integer,
    productid integer,
    validfrom DATE,
    validto DATE,
    version integer
);
