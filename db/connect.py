import psycopg2
conn = psycopg2.connect(dbname='wigay_csi_db', user='postgres', password='wigay', host='localhost', port=5432)
cur = conn.cursor()
cur.execute("SELECT patient_id, name, room_number FROM patients LIMIT 5;")
print(cur.fetchall())
cur.close()
conn.close()