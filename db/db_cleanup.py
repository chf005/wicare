#清理過期資料的腳本，定期執行以保持資料庫的整潔和效能。

import psycopg2
import time

def cleanup():
    conn = psycopg2.connect(host="localhost", database="wigay_csi_db", user="postgres", password="你的密碼")
    cur = conn.cursor()
    try:
        # 只清理 CSI 緩衝，不刪除健康紀錄
        cur.execute("DELETE FROM csi_buffer WHERE timestamp < NOW() - INTERVAL '100 seconds'")
        print(f"🧹 已清理過期波形數據 (刪除筆數: {cur.rowcount})")
        conn.commit()
    except Exception as e:
        print(f"❌ 清理出錯: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    while True:
        cleanup()
        time.sleep(10) # 每 10 秒跑一次