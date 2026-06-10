import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_language():
    print("Loading dim_language...")

    language_df = pd.read_sql("""
        SELECT
            language_id,
            name AS language_name
        FROM language
    """, source_engine)

    language_df = language_df.drop_duplicates(subset=["language_id"])

    existing = pd.read_sql("SELECT language_id FROM dim_language", dw_engine)
    language_df = language_df[~language_df["language_id"].isin(existing["language_id"])]

    if len(language_df) > 0:
        language_df.to_sql("dim_language", con=dw_engine, if_exists="append", index=False)

    print(f"dim_language loaded successfully: {len(language_df)} new rows")


if __name__ == "__main__":
    load_dim_language()