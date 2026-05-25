import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv('DB_HOST','localhost'),
    database=os.getenv('DB_NAME','wigay_csi_db'),
    user=os.getenv('DB_USER','postgres'),
    password=os.getenv('DB_PASSWORD','wigay'),
    port=os.getenv('DB_PORT','5432')
)

def print_columns(table):
    with conn.cursor() as cur:
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position;", (table,))
        rows = cur.fetchall()
        print(f"\nColumns for {table}:")
        for r in rows:
            print(' -', r[0], '(', r[1], ')')

if __name__ == '__main__':
    print_columns('patients')
    print_columns('devices')
    conn.close()
