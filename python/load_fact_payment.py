import pandas as pd
from db_connection import source_engine, dw_engine


def load_fact_payment():
    print("Loading fact_payment...")

    fact_df = pd.read_sql("""
        SELECT
            p.payment_id,
            p.rental_id,

            CAST(DATE_FORMAT(p.payment_date, '%%Y%%m%%d') AS UNSIGNED) AS payment_date_key,

            dc.customer_key,
            df.film_key,
            ds.store_key,
            dst.staff_key,

            p.amount AS payment_amount,
            1 AS payment_count

        FROM payment p
        INNER JOIN rental r
            ON p.rental_id = r.rental_id
        INNER JOIN inventory i
            ON r.inventory_id = i.inventory_id
        INNER JOIN film f
            ON i.film_id = f.film_id

        INNER JOIN movie_rental_dw.dim_customer dc
            ON p.customer_id = dc.customer_id
        INNER JOIN movie_rental_dw.dim_film df
            ON i.film_id = df.film_id
        INNER JOIN movie_rental_dw.dim_store ds
            ON i.store_id = ds.store_id
        INNER JOIN movie_rental_dw.dim_staff dst
            ON p.staff_id = dst.staff_id
    """, source_engine)

    fact_df = fact_df.drop_duplicates(subset=["payment_id"])

    existing = pd.read_sql("SELECT payment_id FROM fact_payment", dw_engine)
    fact_df = fact_df[~fact_df["payment_id"].isin(existing["payment_id"])]

    if len(fact_df) > 0:
        fact_df.to_sql("fact_payment", con=dw_engine, if_exists="append", index=False)

    print(f"fact_payment loaded successfully: {len(fact_df)} new rows")


if __name__ == "__main__":
    load_fact_payment()