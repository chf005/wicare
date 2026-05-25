from flask import Flask, jsonify
from flask_cors import CORS
import db_manager

app = Flask(__name__)
CORS(app)

# 獲取房間狀態 (Image 5)
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify(db_manager.get_room_occupancy())

# 獲取受護者列表 (Image 1, 3)
@app.route('/api/patients', methods=['GET'])
def get_patients():
    return jsonify(db_manager.get_all_patients())

# 獲取健康趨勢 (Image 1 右側圖表)
@app.route('/api/health_trends/<int:pid>', methods=['GET'])
def get_trends(pid):
    return jsonify(db_manager.get_health_trends(pid))

# 獲取即時波形 (CSI 專用)
@app.route('/api/csi/<mac>', methods=['GET'])
def get_csi(mac):
    return jsonify(db_manager.get_recent_csi(mac))

if __name__ == '__main__':
    # 關鍵：將 host 改為 '0.0.0.0'，代表允許區域網路內的所有設備連線
    app.run(debug=True, host='0.0.0.0', port=5000)