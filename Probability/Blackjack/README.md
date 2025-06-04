# ♠️ 21 點（Blackjack）模擬器

🔹 基本玩法：
玩家與莊家各兩張牌

    玩家可點選「Hit（抽牌）」或「Stand（停牌）」

    結果比較點數顯示勝負

    自動處理爆牌、Blackjack、平手

🔹 顯示內容：

    玩家和莊家目前的牌與點數

    遊戲結果（勝 / 負 / 平手）

    重置按鈕：重新開始新的一局

## 🗂️ 專案架構
```js
Blackjack/
├── app.py                 # Flask 主程式
├── static/
│   └── script.js          # 前端互動邏輯 (JavaScript)
│   └── style.css 
├── templates/
│   └── index.html         # 主畫面 HTML

```
```bash
python blackjack_app.py
```
啟動後開啟網頁：http://127.0.0.1:5000  
可進行轉盤
---
## 📜 License

本專案僅供學術研究與個人作品展示，請勿用於商業用途。