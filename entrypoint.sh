#!/bin/sh

# 這個腳本用於處理啟動 Gunicorn 伺服器前的一切準備工作。
# 確保腳本在任何命令失敗時立即退出
set -e

# 定義 Django 設定檔模組的路徑
DJANGO_SETTINGS="DialogueAnchor.settings" # 注意：這裡修正為只包含內層的設定模組

# 為了讓 manage.py 正確找到 settings，我們將工作目錄切換到包含 manage.py 的子目錄。
cd DialogueAnchor/

# 步驟 1: 收集靜態文件
# ***關鍵修正：使用 --settings 旗標明確指定設定模組***
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS

# 步驟 2: 運行資料庫遷移
echo "Running database migrations..."
python manage.py migrate --noinput --settings=$DJANGO_SETTINGS

# 步驟 3: 啟動主程序 (Gunicorn)
# 由於 Gunicorn 需要在應用程式的根目錄（即包含 manage.py 的目錄）啟動，
# 我們不需要切回上層目錄。

# 採用 Python 模組方式啟動 Gunicorn
echo "Starting Gunicorn server via Python module..."

# $1 預期是 'gunicorn'，我們將其移除
shift

# 執行 python -m gunicorn，並將 CMD 的剩餘參數傳入
# 由於現在位於 DialogueAnchor/ 目錄，WSGI 模組可以直接被找到。
exec python -m gunicorn "$@"