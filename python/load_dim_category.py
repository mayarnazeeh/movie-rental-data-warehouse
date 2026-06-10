import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_category():
    print("Loading dim_category...")

    category_df = pd.read_sql("""
        SELECT
            category_id,
            name AS category_name
        FROM category
    """, source_engine)

    category_df = category_df.drop_duplicates(subset=["category_id"])

    existing = pd.read_sql("SELECT category_id FROM dim_category", dw_engine)
    category_df = category_df[~category_df["category_id"].isin(existing["category_id"])]

    if len(category_df) > 0:
        category_df.to_sql("dim_category", con=dw_engine, if_exists="append", index=False)

    print(f"dim_category loaded successfully: {len(category_df)} new rows")


if __name__ == "__main__":
    load_dim_category()