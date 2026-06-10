import pandas as pd
from db_connection import source_engine, dw_engine


def create_date_key(date_value):
    return int(pd.to_datetime(date_value).strftime("%Y%m%d"))


def load_dim_date():
    print("Loading dim_date...")

    dates_df = pd.read_sql("""
        SELECT rental_date AS date_value FROM rental
        UNION
        SELECT return_date AS date_value FROM rental WHERE return_date IS NOT NULL
        UNION
        SELECT payment_date AS date_value FROM payment
    """, source_engine)

    dates_df["date_value"] = pd.to_datetime(dates_df["date_value"]).dt.date
    dates_df = dates_df.drop_duplicates().dropna()

    dim_date = pd.DataFrame()
    dim_date["full_date"] = pd.to_datetime(dates_df["date_value"])
    dim_date["date_key"] = dim_date["full_date"].apply(create_date_key)
    dim_date["day_number"] = dim_date["full_date"].dt.day
    dim_date["day_name"] = dim_date["full_date"].dt.day_name()
    dim_date["month_number"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["quarter_number"] = dim_date["full_date"].dt.quarter
    dim_date["year_number"] = dim_date["full_date"].dt.year

    dim_date = dim_date[
        [
            "date_key",
            "full_date",
            "day_number",
            "day_name",
            "month_number",
            "month_name",
            "quarter_number",
            "year_number"
        ]
    ]

    existing = pd.read_sql("SELECT date_key FROM dim_date", dw_engine)
    dim_date = dim_date[~dim_date["date_key"].isin(existing["date_key"])]

    if len(dim_date) > 0:
        dim_date.to_sql("dim_date", con=dw_engine, if_exists="append", index=False)

    print(f"dim_date loaded successfully: {len(dim_date)} new rows")


if __name__ == "__main__":
    load_dim_date()