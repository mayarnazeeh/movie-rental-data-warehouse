import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_film():
    print("Loading dim_film...")

    film_df = pd.read_sql("""
        SELECT
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            dl.language_key,
            f.rental_duration,
            f.rental_rate,
            f.length,
            f.replacement_cost,
            f.rating
        FROM film f
        LEFT JOIN movie_rental_dw.dim_language dl
            ON f.language_id = dl.language_id
    """, source_engine)

    film_df = film_df.drop_duplicates(subset=["film_id"])

    existing = pd.read_sql("SELECT film_id FROM dim_film", dw_engine)
    film_df = film_df[~film_df["film_id"].isin(existing["film_id"])]

    if len(film_df) > 0:
        film_df.to_sql("dim_film", con=dw_engine, if_exists="append", index=False)

    print(f"dim_film loaded successfully: {len(film_df)} new rows")


if __name__ == "__main__":
    load_dim_film()