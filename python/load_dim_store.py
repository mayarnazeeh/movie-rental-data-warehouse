import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_store():
    print("Loading dim_store...")

    store_df = pd.read_sql("""
        SELECT
            s.store_id,
            s.manager_staff_id,
            a.address,
            ci.city,
            co.country
        FROM store s
        LEFT JOIN address a ON s.address_id = a.address_id
        LEFT JOIN city ci ON a.city_id = ci.city_id
        LEFT JOIN country co ON ci.country_id = co.country_id
    """, source_engine)

    store_df = store_df.drop_duplicates(subset=["store_id"])

    existing = pd.read_sql("SELECT store_id FROM dim_store", dw_engine)
    store_df = store_df[~store_df["store_id"].isin(existing["store_id"])]

    if len(store_df) > 0:
        store_df.to_sql("dim_store", con=dw_engine, if_exists="append", index=False)

    print(f"dim_store loaded successfully: {len(store_df)} new rows")


if __name__ == "__main__":
    load_dim_store()