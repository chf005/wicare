#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 服務器 - 連接 PostgreSQL 數據庫
啟動方式：python server.py
訪問: http://localhost:5000
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

app = Flask(__name__)
CORS(app)

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 數據庫連接配置
DB_CONFIG = {
    'dbname': 'wigay_csi_db',
    'user': 'postgres',
    'password': 'wigay',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    """獲取數據庫連接"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"數據庫連接失敗: {e}")
        raise

# ============================================================================
# 健康檢查端點
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """檢查服務器和數據庫狀態"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'message': '服務器和數據庫連接正常',
            'database': 'wigay_csi_db',
            'host': 'localhost',
            'port': 5432
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'數據庫連接失敗: {str(e)}'
        }), 500

# ============================================================================
# 患者端點
# ============================================================================

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """獲取所有患者信息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                patient_id,
                name,
                gender,
                birth_date,
                age,
                room_number,
                medical_history,
                medications,
                notes
            FROM patients
            ORDER BY patient_id
        """)
        
        patients = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(patients), 200
    except Exception as e:
        logger.error(f"獲取患者列表失敗: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """獲取特定患者信息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                patient_id,
                name,
                gender,
                birth_date,
                age,
                room_number,
                medical_history,
                medications,
                notes
            FROM patients
            WHERE patient_id = %s
        """, (patient_id,))
        
        patient = cur.fetchone()
        cur.close()
        conn.close()
        
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({'error': '患者未找到'}), 404
    except Exception as e:
        logger.error(f"獲取患者信息失敗: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# 房間端點
# ============================================================================

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """獲取所有房間信息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                mac_address,
                device_name,
                room_number,
                current_rssi,
                movement_score,
                occupancy_status,
                last_seen
            FROM rooms
            ORDER BY room_number
        """)
        
        rooms = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(rooms), 200
    except Exception as e:
        logger.error(f"獲取房間列表失敗: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# 數據庫統計端點
# ============================================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """獲取數據庫統計信息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 患者統計
        cur.execute("SELECT COUNT(*) as patient_count FROM patients")
        patient_stats = cur.fetchone()
        
        # 房間統計
        cur.execute("SELECT COUNT(*) as room_count FROM rooms")
        room_stats = cur.fetchone()
        
        # 獲取表列表
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row['table_name'] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'database': 'wigay_csi_db',
            'patients': patient_stats['patient_count'],
            'rooms': room_stats['room_count'],
            'tables': tables,
            'status': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"獲取統計信息失敗: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# 測試端點
# ============================================================================

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """測試數據庫連接"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 執行簡單查詢
        cur.execute("SELECT version()")
        db_version = cur.fetchone()[0]
        
        # 檢查表是否存在
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': '數據庫連接成功',
            'database_version': db_version,
            'tables': tables,
            'config': {
                'dbname': DB_CONFIG['dbname'],
                'user': DB_CONFIG['user'],
                'host': DB_CONFIG['host'],
                'port': DB_CONFIG['port']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'message': '數據庫連接失敗',
            'error': str(e)
        }), 500

# ============================================================================
# 根端點
# ============================================================================

@app.route('/', methods=['GET'])
def root():
    """根端點 - API 信息"""
    return jsonify({
        'name': '智慧長照監控系統 - 數據庫 API',
        'version': '1.0.0',
        'description': '展示 PostgreSQL 數據庫集成',
        'endpoints': [
            {
                'path': '/health',
                'method': 'GET',
                'description': '檢查服務器和數據庫狀態'
            },
            {
                'path': '/api/patients',
                'method': 'GET',
                'description': '獲取所有患者信息'
            },
            {
                'path': '/api/patients/<id>',
                'method': 'GET',
                'description': '獲取特定患者信息'
            },
            {
                'path': '/api/rooms',
                'method': 'GET',
                'description': '獲取所有房間信息'
            },
            {
                'path': '/api/stats',
                'method': 'GET',
                'description': '獲取數據庫統計信息'
            },
            {
                'path': '/api/test-connection',
                'method': 'GET',
                'description': '測試數據庫連接'
            }
        ]
    }), 200

# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║  智慧長照監控系統 - API 服務器                            ║
    ╠════════════════════════════════════════════════════════╣
    ║  數據庫: wigay_csi_db (PostgreSQL)                     ║
    ║  主機: localhost:5432                                  ║
    ║  API 服務器: http://localhost:5000                     ║
    ║                                                        ║
    ║  初始化端點：                                            ║
    ║  ✓ GET  /                          - API 信息          ║
    ║  ✓ GET  /health                    - 健康檢查          ║
    ║  ✓ GET  /api/test-connection       - 測試連接          ║
    ║  ✓ GET  /api/stats                 - 統計信息          ║
    ║  ✓ GET  /api/patients              - 患者列表          ║
    ║  ✓ GET  /api/patients/<id>         - 患者詳情          ║
    ║  ✓ GET  /api/rooms                 - 房間列表          ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print(f"啟動失敗: {e}")
