from load_dim_date import load_dim_date
from load_dim_customer import load_dim_customer
from load_dim_language import load_dim_language
from load_dim_film import load_dim_film
from load_dim_category import load_dim_category
from load_dim_actor import load_dim_actor
from load_dim_store import load_dim_store
from load_dim_staff import load_dim_staff

from load_bridge_film_category import load_bridge_film_category
from load_bridge_film_actor import load_bridge_film_actor

from load_fact_rental import load_fact_rental
from load_fact_payment import load_fact_payment


def run_etl():
    print("Starting ETL process...")

    # Already loaded before. Uncomment only if dim_date is empty.
    # load_dim_date()

    load_dim_customer()
    load_dim_language()
    load_dim_film()
    load_dim_category()
    load_dim_actor()
    load_dim_store()
    load_dim_staff()

    load_bridge_film_category()
    load_bridge_film_actor()

    load_fact_rental()
    load_fact_payment()

    print("ETL process completed successfully!")


if __name__ == "__main__":
    run_etl()