# 今日幸運籤餅 | Daily Fortune Cookie

正能量小程式

## 特色功能 | Features

-  **每日限定** - 一天只能獲得「一個」籤餅，保持神秘感
-  **統計追蹤** - 紀錄連續獲得天數，滿足對連勝的渴望
-  **離線運行** - 無需網路，完全在本地運行

---

## 下載安裝 | Download & Installation

### 方式1：下載可執行檔 | Method 1: Download Executable

1. 前往 **[Actions](../../actions)** 頁面，選擇最新的 run
2. 下載適合系統的版本：
   - **Windows**: `fortune-cookie-windows.zip`
   - **macOS exe版**: `fortune-cookie-macos.zip`
   - **macOS app版**: `fortune-cookie-macos-app.zip`
3. 解壓縮並雙擊執行檔即可使用

### 方式2：從原始碼運行 | Method 2: Run from Source

```bash
# Clone 專案
git clone https://github.com/[your-username]/dailyfortune.git
cd dailyfortune

# 安裝 dependency  
pip install pyinstaller

# 執行
python main.py

# 或建立 executable
python build_universal.py
```

## 使用方法 | How to Use

1. **啟動應用** - 雙擊執行檔開始使用
2. **獲取籤餅** - 點擊「獲取今日籤餅」按鈕
3. **查看統計** - 點擊「查看統計」了解使用記錄
4. **明日再來** - 每天回來獲取新的籤餅！

---

## 首次運行注意事項 | First Run Notes

### Windows 使用者 | Windows Users
- 可能出現「Windows 已保護您的電腦」警告
- 點擊「更多資訊」→「仍要執行」即可

### macOS 使用者 | macOS Users  
- 可能出現「無法驗證開發者」警告
- 右鍵點擊應用程式 → 選擇「打開」→ 點擊「打開」
- 或是前往「設定」 > 「隱私權與安全性」 > 「安全性」，然後點擊右下角的「允許」 按鈕

## 資料儲存 | Data Storage

籤餅歷史記錄儲存在：

- **Windows**: `C:\Users\[使用者名稱]\.dailyfortune\`
- **macOS**: `/Users/[username]/.dailyfortune/`
- **Linux**: `/home/[username]/.dailyfortune/`

### 自動備份功能 | Automatic Backup

應用程式會自動備份您的資料到以下位置，確保更新版本時不會遺失資料：

- **Documents/DailyFortune/backup/**
- **Desktop/DailyFortune_Backup/**
- **Home/DailyFortune_Data/**

**更新步驟**：直接下載新版本並刪除舊資料夾，應用程式會自動復原您的歷史記錄和統計資料。

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
