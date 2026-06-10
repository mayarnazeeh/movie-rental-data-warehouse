import pandas as pd
from db_connection import source_engine, dw_engine


def load_bridge_film_actor():
    print("Loading bridge_film_actor...")

    bridge_df = pd.read_sql("""
        SELECT
            df.film_key,
            da.actor_key
        FROM film_actor fa
        INNER JOIN movie_rental_dw.dim_film df
            ON fa.film_id = df.film_id
        INNER JOIN movie_rental_dw.dim_actor da
            ON fa.actor_id = da.actor_id
    """, source_engine)

    bridge_df = bridge_df.drop_duplicates(subset=["film_key", "actor_key"])

    existing = pd.read_sql("""
        SELECT film_key, actor_key
        FROM bridge_film_actor
    """, dw_engine)

    if len(existing) > 0:
        bridge_df = bridge_df.merge(
            existing,
            on=["film_key", "actor_key"],
            how="left",
            indicator=True
        )
        bridge_df = bridge_df[bridge_df["_merge"] == "left_only"]
        bridge_df = bridge_df[["film_key", "actor_key"]]

    if len(bridge_df) > 0:
        bridge_df.to_sql("bridge_film_actor", con=dw_engine, if_exists="append", index=False)

    print(f"bridge_film_actor loaded successfully: {len(bridge_df)} new rows")


if __name__ == "__main__":
    load_bridge_film_actor()