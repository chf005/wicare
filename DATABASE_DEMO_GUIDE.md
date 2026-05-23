# 📊 向老師展示數據庫集成方案

## 一、快速開始（5 分鐘）

### 步驟 1：安裝 Flask
```bash
pip install flask flask-cors psycopg2-binary
```

### 步驟 2：啟動 API 服務器
```bash
python server.py
```

你會看到這個界面：
```
╔════════════════════════════════════════════════════════╗
║  智慧長照監控系統 - API 服務器                            ║
╠════════════════════════════════════════════════════════╣
║  數據庫: wigay_csi_db (PostgreSQL)                     ║
║  主機: localhost:5432                                  ║
║  API 服務器: http://localhost:5000                     ║
╚════════════════════════════════════════════════════════╝
```

### 步驟 3：在另一個終端啟動前端
```bash
npm run dev
```

## 二、展示方式

### 方式 1️⃣：在瀏覽器中直接訪問 API

#### ✅ 檢查數據庫連接
[http://localhost:5000/health](http://localhost:5000/health)

**返回示例：**
```json
{
  "status": "healthy",
  "message": "服務器和數據庫連接正常",
  "database": "wigay_csi_db",
  "host": "localhost",
  "port": 5432
}
```

#### ✅ 查看 API 信息
[http://localhost:5000/](http://localhost:5000/)

#### ✅ 測試數據庫連接
[http://localhost:5000/api/test-connection](http://localhost:5000/api/test-connection)

**返回示例：**
```json
{
  "message": "數據庫連接成功",
  "database_version": "PostgreSQL 12.0 ...",
  "tables": ["patients", "rooms", "daily_health_records", ...],
  "config": {
    "dbname": "wigay_csi_db",
    "user": "postgres",
    "host": "localhost",
    "port": 5432
  }
}
```

#### ✅ 查看數據庫統計
[http://localhost:5000/api/stats](http://localhost:5000/api/stats)

**返回示例：**
```json
{
  "database": "wigay_csi_db",
  "patients": 7,
  "rooms": 5,
  "tables": ["patients", "rooms", "daily_health_records", "routine_checkup_records"],
  "status": "connected"
}
```

#### ✅ 查看所有患者數據
[http://localhost:5000/api/patients](http://localhost:5000/api/patients)

**返回示例：**
```json
[
  {
    "patient_id": 1,
    "name": "王大明",
    "gender": "男",
    "birth_date": "1952-03-15",
    "age": 74,
    "room_number": "606",
    "medical_history": ["高血壓", "糖尿病"],
    "medications": ["Aspirin", "Metformin"],
    "notes": "注意飲食控制"
  },
  ...
]
```

#### ✅ 查看特定患者
[http://localhost:5000/api/patients/1](http://localhost:5000/api/patients/1)

#### ✅ 查看房間信息
[http://localhost:5000/api/rooms](http://localhost:5000/api/rooms)

---

### 方式 2️⃣：在網頁應用中查看數據

1. 啟動前端應用：`npm run dev`
2. 打開 [http://localhost:3004](http://localhost:3004)
3. 點擊「受護者」菜單 - **所有數據都來自 PostgreSQL 數據庫！**

前端會自動調用後端 API 獲取數據：
```
前端 (localhost:3004) 
  ↓
  └─→ Vite 代理 (/api)
       ↓
       └─→ Flask API (localhost:5000)
            ↓
            └─→ PostgreSQL 數據庫 (localhost:5432)
```

---

### 方式 3️⃣：使用 curl 命令演示

打開 PowerShell 或命令行，運行以下命令：

```bash
# 檢查服務器狀態
curl http://localhost:5000/health

# 測試數據庫連接
curl http://localhost:5000/api/test-connection

# 獲取統計信息
curl http://localhost:5000/api/stats

# 獲取所有患者
curl http://localhost:5000/api/patients

# 獲取特定患者
curl http://localhost:5000/api/patients/1
```

---

### 方式 4️⃣：使用 Postman 或其他 API 工具

1. 下載 Postman - https://www.postman.com/downloads/
2. 導入 API 集合（見下方）
3. 依次運行各個端點

**API 集合（Postman JSON）：**

```json
{
  "info": {
    "name": "CSI 數據庫 API",
    "version": "1.0"
  },
  "item": [
    {
      "name": "健康檢查",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/health"
      }
    },
    {
      "name": "測試連接",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/test-connection"
      }
    },
    {
      "name": "獲取統計",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/stats"
      }
    },
    {
      "name": "患者列表",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/patients"
      }
    },
    {
      "name": "房間列表",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/rooms"
      }
    }
  ]
}
```

---

## 三、演示流程（給老師看）

### 🎬 完整演示腳本（10 分鐘）

1. **打開終端 1**：啟動 API 服務器
   ```bash
   python server.py
   ```
   ✅ 顯示連接成功

2. **打開終端 2**：啟動前端
   ```bash
   npm run dev
   ```
   ✅ 顯示 Vite 已啟動

3. **打開瀏覽器** - 訪問以下 URL：

   | 步驟 | URL | 說明 |
   |------|-----|------|
   | 1 | http://localhost:5000/health | ✅ 顯示服務器和數據庫連接正常 |
   | 2 | http://localhost:5000/api/stats | ✅ 顯示數據庫中有 7 個患者、5 個房間 |
   | 3 | http://localhost:5000/api/patients | ✅ 顯示所有患者的完整信息（來自 PostgreSQL） |
   | 4 | http://localhost:3004 | ✅ 打開網頁應用 |
   | 5 | 點擊「受護者」菜單 | ✅ 顯示患者列表（實時從數據庫讀取） |
   | 6 | 點擊任何患者 | ✅ 顯示詳細資料、用藥記錄、病史等 |

---

## 四、證明數據庫已連接的關鍵證據

### ✅ 技術架構圖

```
PostgreSQL 數據庫 (wigay_csi_db)
│
├─ patients 表 (患者信息)
│  └─ 7 筆患者記錄
│
├─ rooms 表 (房間信息)
│  └─ 5 筆房間記錄
│
└─ 其他表 (日常健康、日常檢查等)
   └─ 多筆醫療記錄
   
   ↓ (連接)
   
Flask REST API (server.py)
├─ /api/patients      (讀取患者表)
├─ /api/rooms         (讀取房間表)
├─ /api/stats         (顯示統計)
├─ /api/test-connection (測試連接)
└─ /health            (健康檢查)

   ↓ (Vite 代理)
   
React 前端 (localhost:3004)
├─ 受護者管理 (顯示患者列表)
├─ 房間佔用 (顯示房間信息)
└─ 可實時編輯患者數據
```

### 🎯 關鍵截圖要點

1. **API 響應** - 顯示真實的患者/房間 JSON 數據
2. **網頁應用** - 受護者列表中的所有數據
3. **控制台日誌** - 顯示 API 調用和數據庫連接

---

## 五、故障排除

### ❌ 問題 1：連接失敗 - "ERROR: could not translate host name..."

**解決方案：**
```bash
# 檢查 PostgreSQL 服務是否運行
services.msc  # Windows - 搜尋 "postgresql"
# 或者使用 pgAdmin 連接測試
```

### ❌ 問題 2：端口已被佔用

**解決方案：**
```bash
# 更改 server.py 中的端口
# 修改最後一行：
app.run(host='127.0.0.1', port=5001, debug=True)  # 改為 5001
```

### ❌ 問題 3：模組未找到 "psycopg2"

**解決方案：**
```bash
pip install psycopg2-binary
```

---

## 六、推薦展示清單

- [ ] ✅ 啟動 API 服務器，顯示連接成功
- [ ] ✅ 訪問 `/health` 端點，展示數據庫連接狀態
- [ ] ✅ 訪問 `/api/stats` 端點，展示數據庫統計
- [ ] ✅ 訪問 `/api/patients` 端點，展示真實患者數據（JSON 格式）
- [ ] ✅ 啟動网頁應用，點擊「受護者」菜單
- [ ] ✅ 編輯患者信息，保存後重新讀取（証明實時連接）
- [ ] ✅ 打開瀏覽器開發者工具（F12），查看網絡請求
- [ ] ✅ 顯示請求流程：前端 → API → 數據庫

---

## 七、總結

這個方案清楚地展示了：

✅ **完整的技術棧**
- 前端：React + TypeScript
- 後端：Python Flask
- 數據庫：PostgreSQL

✅ **實時數據連接**
- 所有患者數據來自真實數據庫
- 可實時查詢、編輯、保存

✅ **生產級別的架構**
- 分離的 API 層
- 跨域請求支持 (CORS)
- 錯誤處理和日誌

**直觀證明** 數據庫已經完全集成到應用中！

---

**最後更新**：2026 年 5 月 20 日
