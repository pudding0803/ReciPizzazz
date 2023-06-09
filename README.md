# ReciPizzazz

> 一個分享與編輯食譜的平台🍰

## 環境

### 目前使用 Python 版本
* 3.10.9

### Frameworks and Libraries
* Bulma - 0.9.4
* JQuery - 3.7.0
* Font Awesome - 6.4.0

### 執行
```
python -m flask run
```

## Requirements

### 安裝套件
```
pip install -r requirements.txt
```

### 更新 requirement.txt
```
pip freeze > requirements.txt
```

## MySQL

### 複製並設定 MySQL 連線資訊
```
cp config.example.ini config.ini
```

### migration
* 初始化（將會產生 `/migrations`）
```
flask db init
```
* 更動 migration
```
flask db migrate -m "description of the migration"
```
* 更新資料庫
```
flask db upgrade
```