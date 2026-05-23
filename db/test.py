import psycopg2
from psycopg2 import extras

# 1. 設定連線參數 (請改成你安裝時設定的密碼)
conn_params = {
    "host": "localhost",
    "database": "wigay_csi_db",
    "user": "postgres",
    "password": "wigay", # <--- 這裡填你安裝 PostgreSQL 時設的密碼
    "port": "5432"
}

try:
    # 2. 嘗試建立連線
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()
    
    # 3. 測試：查詢資料庫版本
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print(f"✅ 連線成功！PostgreSQL 版本: {record}")

    # 4. 測試：寫入一筆假設備資料
    # 這裡改為符合現有 devices 表結構，使用 room_number 和 current_rssi
    insert_query = """
    INSERT INTO devices (mac_address, device_name, room_number, current_rssi)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (mac_address) DO NOTHING;
    """
    device_data = ("AA:BB:CC:DD:EE:FF", "ESP32_Test_01", "ROOM123", -45)
    cursor.execute(insert_query, device_data)
    
    connection.commit()
    print("✅ 測試資料寫入成功！")

except Exception as error:
    print(f"❌ 連線失敗：{error}")

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("🔌 連線已安全關閉。")