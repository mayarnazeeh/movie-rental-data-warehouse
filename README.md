# Movie Rental Data Warehouse

This project was created for the Data Warehousing assignment. It is based on a movie rental OLTP database. The main goal of the project is to redesign the operational database into a dimensional data warehouse that can be used for analysis and reporting. The data warehouse helps answer business questions about movie rentals, revenue, customer activity, film popularity, store performance, staff performance, and trends over time.

The project was implemented using MySQL and Python. MySQL was used to store both the original source database and the data warehouse database. Python was used to build the ETL process, where data is extracted from the OLTP database, transformed into a cleaner analytical format, and loaded into the data warehouse tables.

The dimensional model is designed as a hybrid star schema. The main fact tables are `fact_rental` and `fact_payment`. These fact tables are connected to shared dimension tables such as `dim_date`, `dim_customer`, `dim_film`, `dim_store`, and `dim_staff`. Additional dimensions such as `dim_language`, `dim_category`, and `dim_actor` are used to support film-related analysis. Bridge tables are used to handle the many-to-many relationships between films and categories, and between films and actors.

## Main steps

1. Import the OLTP movie rental database into MySQL.
2. Create the data warehouse database and schema.
3. Build dimension tables and fact tables.
4. Run the Python ETL scripts.
5. Validate the loaded data using row counts.
6. Run analysis queries to answer business questions.
7. Prepare the report, diagram, and screenshots.

## Tools used

- MySQL Workbench
- Python
- Pandas
- SQLAlchemy
- PyMySQL
- Draw.io

## Important files

- `sql/01_create_databases.sql`: creates the source and warehouse databases.
- `sql/02_create_dw_schema.sql`: creates the dimension, fact, and bridge tables.
- `sql/03_analysis_queries.sql`: contains analytical SQL queries.
- `python/Etl.py`: runs the ETL process.
- `python/db_connection.py`: contains the database connection settings.
- `diagrams/dimensional_model.png`: shows the dimensional model.
- `docs/report.pdf`: contains the final assignment report.
- `docs/screenshots/`: contains screenshots for validation and query results.

## How to run

Before running the ETL, update the MySQL password inside `python/db_connection.py`.

Then run:

```bash
python python/Etl.py