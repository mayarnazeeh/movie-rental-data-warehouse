import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_actor():
    print("Loading dim_actor...")

    actor_df = pd.read_sql("""
        SELECT
            actor_id,
            CONCAT(first_name, ' ', last_name) AS actor_full_name
        FROM actor
    """, source_engine)

    actor_df = actor_df.drop_duplicates(subset=["actor_id"])

    existing = pd.read_sql("SELECT actor_id FROM dim_actor", dw_engine)
    actor_df = actor_df[~actor_df["actor_id"].isin(existing["actor_id"])]

    if len(actor_df) > 0:
        actor_df.to_sql("dim_actor", con=dw_engine, if_exists="append", index=False)

    print(f"dim_actor loaded successfully: {len(actor_df)} new rows")


if __name__ == "__main__":
    load_dim_actor()