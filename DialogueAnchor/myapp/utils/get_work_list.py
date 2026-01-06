# myapp/utils/f.py

# 確保 Work 模型的匯入路徑仍是正確的：
from ..models import Work 
from django.core.serializers import serialize
import json

# ... 保持 initialize_default_works 函式不變 ...

def get_all_works_json_for_template():
    """
    獲取所有 Work 模型的 id 和 work_name，並轉換為 JSON 格式的字串。
    這個 JSON 字串可以直接傳遞給 Django 模板，供前端 JavaScript 使用。
    """
    # 1. 獲取 queryset，只選取 'id' 和 'work_name' 欄位，減少資料傳輸量
    works_queryset = Work.objects.all().values('id', 'work_name')
    
    # 2. 將 QuerySet 轉換成 List of Dicts
    #    雖然可以使用 Django 的 serialize，但直接轉換成簡單的 dict 列表通常更高效：
    works_list = list(works_queryset)
    
    # 3. 將 Python 列表轉換為 JSON 字串
    #    Django 的模板可以直接處理 Python list/dict，但為了明確傳遞 JSON 資料，
    #    我們可以在這裡轉換，或留給 View 處理。這裡我們直接轉換成字串。
    return json.dumps(works_list)