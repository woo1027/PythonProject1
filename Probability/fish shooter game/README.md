# 🎣 魚機（Fish Shooter Game）

每次射擊消耗一發子彈（成本1）。

若隨機機率小於魚的出現機率 (prob)，則算擊中，賺取魚的獎勵 (reward) 減去子彈成本。

否則沒擊中，只損失子彈成本。

## 📁 結構
```
fish_shooter_game/
├── fish_app.py                ← Flask 主伺服器
└── templates/
    └── index.html        ← 前端介面
```


```bash
python fish_app.py
```
啟動後開啟網頁：http://127.0.0.1:5000  
可進行魚機
---




## 📜 License

本專案僅供學術研究與個人作品展示，請勿用於商業用途。