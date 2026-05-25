#加入測試資料的腳本，這些資料將用於測試 `delete_expired_data` 函式是否能正確刪除過期資料並保留新鮮資料。

import os
import psycopg2
from psycopg2 import extras
import json

conn_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "wigay_csi_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "wigay"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    return psycopg2.connect(**conn_params)


def seed():
    """Insert minimal seed data: users, patients, devices."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Insert users (basic)
            cur.execute("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES
            ('admin', 'admin-hash', '系統管理者', 'admin'),
            ('medic1', 'medic-hash', '林小明', 'medic'),
            ('family1', 'family-hash', '王太太', 'family')
            ON CONFLICT (username) DO NOTHING;
            """)

            # Get existing patient columns
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='patients';")
            patient_cols = {r[0] for r in cur.fetchall()}

            # Prepare patient insert depending on available columns
            if {'name', 'age', 'room_number', 'family_id', 'medic_id'}.issubset(patient_cols):
                cur.execute("""
                INSERT INTO patients (name, age, room_number, family_id, medic_id)
                VALUES
                ('王大明', 78, '204', (SELECT user_id FROM users WHERE username='family1'), (SELECT user_id FROM users WHERE username='medic1')),
                ('陳老太', 85, '205', (SELECT user_id FROM users WHERE username='family1'), (SELECT user_id FROM users WHERE username='medic1'))
                ON CONFLICT (patient_id) DO NOTHING;
                """)
            else:
                # Fallback: insert minimal columns dynamically using parameterized queries
                cols = ['name']
                if 'age' in patient_cols:
                    cols.append('age')
                if 'room_number' in patient_cols:
                    cols.append('room_number')

                patients_list = []
                for name, age, room in [('王大明', 78, '204'), ('陳老太', 85, '205')]:
                    row = [name]
                    if 'age' in patient_cols:
                        row.append(age)
                    if 'room_number' in patient_cols:
                        row.append(room)
                    patients_list.append(tuple(row))

                placeholders = ', '.join(['%s'] * len(cols))
                insert_sql = f"INSERT INTO patients ({', '.join(cols)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
                try:
                    cur.executemany(insert_sql, patients_list)
                except Exception:
                    # safety: rollback and insert names only
                    conn.rollback()
                    cur.execute("INSERT INTO patients (name) VALUES (%s),(%s) ON CONFLICT DO NOTHING;", ('王大明', '陳老太'))

            # Insert devices matching existing schema
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='devices';")
            device_cols = {r[0] for r in cur.fetchall()}

            # Decide which columns to insert
            dev_cols = ['mac_address', 'device_name']
            if 'room_number' in device_cols:
                dev_cols.append('room_number')
            if 'movement_score' in device_cols:
                dev_cols.append('movement_score')
            if 'current_rssi' in device_cols:
                dev_cols.append('current_rssi')

            placeholders = ', '.join(['%s'] * len(dev_cols))
            col_list = ', '.join(dev_cols)
            dev_values = [
                ('AA:BB:CC:DD:EE:01', 'ESP32_Room204', '204', 12, -50),
                ('AA:BB:CC:DD:EE:02', 'ESP32_Room205', '205', 3, -70)
            ]

            # Map values to available columns
            for dv in dev_values:
                mapped = []
                # dv order: mac, name, room, movement, rssi
                for idx, c in enumerate(dev_cols):
                    if c == 'mac_address': mapped.append(dv[0])
                    elif c == 'device_name': mapped.append(dv[1])
                    elif c == 'room_number': mapped.append(dv[2])
                    elif c == 'movement_score': mapped.append(dv[3])
                    elif c == 'current_rssi': mapped.append(dv[4])
                cur.execute(f"INSERT INTO devices ({col_list}) VALUES ({placeholders}) ON CONFLICT (mac_address) DO NOTHING;", tuple(mapped))

            conn.commit()


if __name__ == '__main__':
    print('Seeding database...')
    try:
        seed()
        print('Seeding completed.')
    except Exception as e:
        print('Seeding failed:', e)

# --- 網頁功能 1：獲取所有受護者列表 ---
def get_all_patients():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM patients ORDER BY room_number ASC;")
            return cur.fetchall()

# --- 網頁功能 2：獲取特定受護者的健康趨勢 (對應 UI 趨勢圖) ---
def get_health_trends(patient_id, days=7):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            sql = """
            SELECT measured_at::date as date, systolic_bp, diastolic_bp, blood_sugar, weight
            FROM health_records
            WHERE patient_id = %s AND measured_at > NOW() - INTERVAL '%s days'
            ORDER BY measured_at ASC;
            """
            cur.execute(sql, (patient_id, days))
            return cur.fetchall()

# --- 網頁功能 3：獲取房間佔用狀態 (對應 UI 總覽卡片) ---
def get_room_occupancy():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM devices ORDER BY room_number ASC;")
            return cur.fetchall()

# --- 核心功能：CSI 緩衝抓取 (維持原有機制) ---
def get_recent_csi(device_mac):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            sql = "SELECT timestamp, csi_payload FROM csi_buffer WHERE device_id = %s AND timestamp > NOW() - INTERVAL '100 seconds' ORDER BY timestamp ASC;"
            cur.execute(sql, (device_mac,))
            return cur.fetchall()