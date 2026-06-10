import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_customer():
    print("Loading dim_customer...")

    customer_df = pd.read_sql("""
        SELECT
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_full_name,
            c.email,
            CASE
                WHEN c.active = 1 THEN 'Active'
                ELSE 'Inactive'
            END AS active_status,
            a.address,
            ci.city,
            co.country,
            DATE(c.create_date) AS create_date
        FROM customer c
        LEFT JOIN address a ON c.address_id = a.address_id
        LEFT JOIN city ci ON a.city_id = ci.city_id
        LEFT JOIN country co ON ci.country_id = co.country_id
    """, source_engine)

    customer_df = customer_df.drop_duplicates(subset=["customer_id"])

    existing = pd.read_sql("SELECT customer_id FROM dim_customer", dw_engine)
    customer_df = customer_df[~customer_df["customer_id"].isin(existing["customer_id"])]

    if len(customer_df) > 0:
        customer_df.to_sql("dim_customer", con=dw_engine, if_exists="append", index=False)

    print(f"dim_customer loaded successfully: {len(customer_df)} new rows")


if __name__ == "__main__":
    load_dim_customer()