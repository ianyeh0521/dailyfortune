# 今日幸運籤餅 | Daily Fortune Cookie

正能量小程式

## 特色功能 | Features

-  **每日限定** - 一天只能獲得一個籤餅，保持神秘感
-  **統計追蹤** - 記錄您的連續天數和總籤餅數
-  **豐富內容** - 超過 100條精心挑選的勵志訊息
-  **離線運行** - 無需網路連線，完全本地運行
-  **隱私保護** - 所有資料儲存在本地，絕不上傳


## 下載安裝 | Download & Installation

### 方式1：下載可執行檔 | Method 1: Download Executable

1. 前往 **[Releases](../../releases)** 頁面
2. 下載適合您系統的版本：
   - **Windows**: `今日幸運籤餅-Windows.zip`
   - **macOS**: `今日幸運籤餅-macOS.zip`
3. 解壓縮並雙擊執行檔即可使用

### 方式2：從原始碼運行 | Method 2: Run from Source

```bash
# Clone the project
git clone https://github.com/[your-username]/dailyfortune.git
cd dailyfortune

# Install dependencies  
pip install pyinstaller

# Run directly
python main.py

# Or build executable
python build_universal.py
```

## 使用方法 | How to Use

1. **啟動應用** - 雙擊執行檔開始使用
2. **獲取籤餅** - 點擊「獲取今日籤餅」按鈕
3. **查看統計** - 點擊「查看統計」了解您的使用記錄
4. **明日再來** - 每天回來獲取新的籤餅！

---

1. **Launch App** - Double-click the executable to start
2. **Get Fortune** - Click "Get Today's Fortune Cookie" button
3. **View Stats** - Click "View Statistics" to see your usage record
4. **Come Back Tomorrow** - Return daily for new fortune cookies!

## 首次運行注意事項 | First Run Notes

### Windows 使用者 | Windows Users
- 可能出現「Windows 已保護您的電腦」警告
- 點擊「更多資訊」→「仍要執行」即可

### macOS 使用者 | macOS Users  
- 可能出現「無法驗證開發者」警告
- 右鍵點擊應用程式 → 選擇「打開」→ 點擊「打開」

## 資料儲存 | Data Storage

您的籤餅歷史記錄儲存在：

Your fortune history is stored at:

- **Windows**: `C:\Users\[使用者名稱]\.dailyfortune\`
- **macOS**: `/Users/[username]/.dailyfortune/`
- **Linux**: `/home/[username]/.dailyfortune/`


### 建置狀態 | Build Status
![Build Status](../../actions/workflows/build.yml/badge.svg)

### 專案結構 | Project Structure
```
dailyfortune/
├── main.py              # 主程式入口
├── gui.py               # 使用者界面
├── fortune_data.py      # 資料管理
├── fortunes.json        # 籤餅資料庫
├── build_universal.py   # 建置腳本
└── .github/workflows/   # GitHub Actions
```
