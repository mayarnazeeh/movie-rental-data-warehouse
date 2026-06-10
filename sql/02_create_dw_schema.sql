USE movie_rental_dw;

DROP TABLE IF EXISTS fact_payment;
DROP TABLE IF EXISTS fact_rental;

DROP TABLE IF EXISTS bridge_film_actor;
DROP TABLE IF EXISTS bridge_film_category;

DROP TABLE IF EXISTS dim_staff;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_actor;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_film;
DROP TABLE IF EXISTS dim_language;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_number INT,
    day_name VARCHAR(20),
    month_number INT,
    month_name VARCHAR(20),
    quarter_number INT,
    year_number INT
);

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_full_name VARCHAR(150),
    email VARCHAR(100),
    active_status VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    create_date DATE
);

CREATE TABLE dim_language (
    language_key INT AUTO_INCREMENT PRIMARY KEY,
    language_id INT NOT NULL,
    language_name VARCHAR(50)
);

CREATE TABLE dim_film (
    film_key INT AUTO_INCREMENT PRIMARY KEY,
    film_id INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    release_year INT,
    language_key INT,
    rental_duration INT,
    rental_rate DECIMAL(6,2),
    length INT,
    replacement_cost DECIMAL(8,2),
    rating VARCHAR(20),

    FOREIGN KEY (language_key) REFERENCES dim_language(language_key)
);

CREATE TABLE dim_category (
    category_key INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    category_name VARCHAR(100)
);

CREATE TABLE dim_actor (
    actor_key INT AUTO_INCREMENT PRIMARY KEY,
    actor_id INT NOT NULL,
    actor_full_name VARCHAR(150)
);

CREATE TABLE dim_store (
    store_key INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT NOT NULL,
    manager_staff_id INT,
    address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE dim_staff (
    staff_key INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT NOT NULL,
    staff_full_name VARCHAR(150),
    email VARCHAR(100),
    active_status VARCHAR(20),
    store_id INT,
    address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE bridge_film_category (
    film_key INT NOT NULL,
    category_key INT NOT NULL,

    PRIMARY KEY (film_key, category_key),

    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key)
);

CREATE TABLE bridge_film_actor (
    film_key INT NOT NULL,
    actor_key INT NOT NULL,

    PRIMARY KEY (film_key, actor_key),

    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (actor_key) REFERENCES dim_actor(actor_key)
);

CREATE TABLE fact_rental (
    rental_fact_key INT AUTO_INCREMENT PRIMARY KEY,
    rental_id INT NOT NULL,

    rental_date_key INT NOT NULL,
    return_date_key INT NULL,

    customer_key INT NOT NULL,
    film_key INT NOT NULL,
    store_key INT NOT NULL,
    staff_key INT NOT NULL,

    rental_count INT DEFAULT 1,
    rental_duration_days INT,
    expected_rental_duration INT,
    late_return_flag TINYINT,

    FOREIGN KEY (rental_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (return_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key)
);

CREATE TABLE fact_payment (
    payment_fact_key INT AUTO_INCREMENT PRIMARY KEY,
    payment_id INT NOT NULL,
    rental_id INT,

    payment_date_key INT NOT NULL,

    customer_key INT NOT NULL,
    film_key INT NOT NULL,
    store_key INT NOT NULL,
    staff_key INT NOT NULL,

    payment_amount DECIMAL(10,2),
    payment_count INT DEFAULT 1,

    FOREIGN KEY (payment_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key)
);