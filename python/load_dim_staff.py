import pandas as pd
from db_connection import source_engine, dw_engine


def load_dim_staff():
    print("Loading dim_staff...")

    staff_df = pd.read_sql("""
        SELECT
            st.staff_id,
            CONCAT(st.first_name, ' ', st.last_name) AS staff_full_name,
            st.email,
            CASE
                WHEN st.active = 1 THEN 'Active'
                ELSE 'Inactive'
            END AS active_status,
            st.store_id,
            a.address,
            ci.city,
            co.country
        FROM staff st
        LEFT JOIN address a ON st.address_id = a.address_id
        LEFT JOIN city ci ON a.city_id = ci.city_id
        LEFT JOIN country co ON ci.country_id = co.country_id
    """, source_engine)

    staff_df = staff_df.drop_duplicates(subset=["staff_id"])

    existing = pd.read_sql("SELECT staff_id FROM dim_staff", dw_engine)
    staff_df = staff_df[~staff_df["staff_id"].isin(existing["staff_id"])]

    if len(staff_df) > 0:
        staff_df.to_sql("dim_staff", con=dw_engine, if_exists="append", index=False)

    print(f"dim_staff loaded successfully: {len(staff_df)} new rows")


if __name__ == "__main__":
    load_dim_staff()