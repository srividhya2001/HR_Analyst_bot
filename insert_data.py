import pandas as pd
from sqlalchemy import create_engine

# --- PostgreSQL connection ---
USER = "postgres"
PASSWORD = "srividhya"
HOST = "localhost"
PORT = "5432"
DATABASE = "postgres"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# --- Base folder path ---
BASE_PATH = "/Users/devbabu/Downloads/SriVidhya-DiscountTire-Assessment"

files = {
    "demographics": f"{BASE_PATH}/demographics.csv",
    "location": f"{BASE_PATH}/location.csv",
    "workinfo": f"{BASE_PATH}/workinfo.csv",
    "storeincome": f"{BASE_PATH}/storeincome.csv"
}

for table, file_path in files.items():
    # Read CSV instead of Excel
    df = pd.read_csv(file_path)

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # Fix for storeincome table only
    if table == "storeincome":
        if "date" in df.columns:
            df.rename(columns={"date": "date_qtr"}, inplace=True)

    # Insert into PostgreSQL
    df.to_sql(table, engine, if_exists="append", index=False)

    print(f"Inserted {len(df)} rows into {table}")