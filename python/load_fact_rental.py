import pandas as pd
from db_connection import source_engine, dw_engine


def load_fact_rental():
    print("Loading fact_rental...")

    fact_df = pd.read_sql("""
        SELECT
            r.rental_id,

            CAST(DATE_FORMAT(r.rental_date, '%%Y%%m%%d') AS UNSIGNED) AS rental_date_key,
            CASE
                WHEN r.return_date IS NOT NULL
                THEN CAST(DATE_FORMAT(r.return_date, '%%Y%%m%%d') AS UNSIGNED)
                ELSE NULL
            END AS return_date_key,

            dc.customer_key,
            df.film_key,
            ds.store_key,
            dst.staff_key,

            1 AS rental_count,

            CASE
                WHEN r.return_date IS NOT NULL
                THEN DATEDIFF(r.return_date, r.rental_date)
                ELSE NULL
            END AS rental_duration_days,

            f.rental_duration AS expected_rental_duration,

            CASE
                WHEN r.return_date IS NOT NULL
                     AND DATEDIFF(r.return_date, r.rental_date) > f.rental_duration
                THEN 1
                ELSE 0
            END AS late_return_flag

        FROM rental r
        INNER JOIN customer c
            ON r.customer_id = c.customer_id
        INNER JOIN inventory i
            ON r.inventory_id = i.inventory_id
        INNER JOIN film f
            ON i.film_id = f.film_id

        INNER JOIN movie_rental_dw.dim_customer dc
            ON r.customer_id = dc.customer_id
        INNER JOIN movie_rental_dw.dim_film df
            ON i.film_id = df.film_id
        INNER JOIN movie_rental_dw.dim_store ds
            ON i.store_id = ds.store_id
        INNER JOIN movie_rental_dw.dim_staff dst
            ON r.staff_id = dst.staff_id
    """, source_engine)

    fact_df = fact_df.drop_duplicates(subset=["rental_id"])

    existing = pd.read_sql("SELECT rental_id FROM fact_rental", dw_engine)
    fact_df = fact_df[~fact_df["rental_id"].isin(existing["rental_id"])]

    if len(fact_df) > 0:
        fact_df.to_sql("fact_rental", con=dw_engine, if_exists="append", index=False)

    print(f"fact_rental loaded successfully: {len(fact_df)} new rows")


if __name__ == "__main__":
    load_fact_rental()