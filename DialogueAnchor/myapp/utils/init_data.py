# myapp/utils/f.py

# 關鍵變動：使用 ..models 來跳出 utils/ 目錄，找到上層的 models.py
from ..models import Work 

def initialize_default_works():
    """
    初始化預設的工作資料 (Work)。
    如果資料庫中 Work 欄位不存在，則創建它。
    """
    default_works = [
        "mygo",
        "ave mujica",
        "test2",
        "test3",
        "test4",
    ]
    
    print("正在檢查並初始化預設工作資料...")
    
    for work_name in default_works:
        work, created = Work.objects.get_or_create(
            work_name=work_name
        )
        
        if created:
            print(f"成功創建新的工作項目: {work_name}")
            
    print("預設工作資料初始化完成。")