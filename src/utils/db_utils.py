import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment variables
load_dotenv()

USER = os.getenv("user")
PASSWORD = urllib.parse.quote_plus(os.getenv("password"))
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


def write_table(df, schema, table_name):
    """Write dataframe to PostgreSQL (overwrite table)."""
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                schema=schema,
                if_exists="replace",
                index=False,
                method="multi"
            )

        print(f"Table {schema}.{table_name} written successfully.")

    except Exception as e:
        raise Exception(f"Write failed: {e}")

    finally:
        engine.dispose()


def read_table(query):
    """Read SQL query into pandas dataframe."""

    engine = create_engine(DATABASE_URL)

    try:
        df = pd.read_sql(query, engine)
        return df

    except Exception as e:
        raise Exception(f"Read failed: {e}")

    finally:
        engine.dispose()