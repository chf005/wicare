# 這個程式是用來測試從資料庫抓取最近 100 秒的 CSI 資料，並且印出來看看格式。

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

# --- 網頁功能 4：獲取所有使用者列表 ---
def get_all_users():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT user_id, username, full_name, role, created_at FROM users ORDER BY user_id ASC;")
            return cur.fetchall()

# --- 網頁功能 5：獲取特定使用者資訊 ---
def get_user_by_id(user_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute("SELECT user_id, username, full_name, role, created_at FROM users WHERE user_id = %s;", (user_id,))
            return cur.fetchone()
