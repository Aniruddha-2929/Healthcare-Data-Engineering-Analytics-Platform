import pandas as pd
from src.db_connection import get_connection
from src.data_validation import validate_patients, validate_doctors, validate_visits, validate_lab_reports


def load_csv_to_mysql(file_path, table_name, validator=None):
    """
    Load a CSV file into a MySQL table.
    Optionally applies a validation function before insertion.
    """
    df = pd.read_csv(file_path)

    if validator:
        df = validator(df)

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(df.columns)
        sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"  [OK] Loaded {len(df)} rows into `{table_name}`")
