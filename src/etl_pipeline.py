import pandas as pd
from src.db_connection import get_connection


def load_csv_to_mysql(table_name, file_path):
    """
    Utility function to load a CSV file directly into MySQL
    without validation. Used for quick data loads.
    """
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        columns = ", ".join(df.columns)

        sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"  [OK] Loaded {len(df)} rows into `{table_name}` (no validation)")
