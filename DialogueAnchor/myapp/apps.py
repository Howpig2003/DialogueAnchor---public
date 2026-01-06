from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    def ready(self):
        # 關鍵變動：使用 .utils.init_data 匯入子目錄 utils/ 下的 init_data.py 檔案
        from .utils.init_data import initialize_default_works
        
        # 呼叫初始化函式
        try:
            initialize_default_works()
        except Exception as e:
            # 確保處理資料庫尚未準備好的情況
            print(f"初始化預設工作資料時發生錯誤: {e}")