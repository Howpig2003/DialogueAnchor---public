# app_name/utils/f.py

# 匯入必要的函式庫
import requests, os
import json
from ..models import Work # 假設 Work 仍然會在這裡使用 (保持不變)
QUERY_KEY = os.environ.get('query_key', 'your-query-key')
# 🚨 請替換成您要呼叫的 API 端點 URL
# 假設 API 是這樣: API_URL?work_id=...&text=...
API_ENDPOINT_URL = os.environ.get('api_query_url', 'https://example.com/api/query_image')


# ... (保持 initialize_default_works 函式不變) ...
# ... (保持 get_all_works_json_for_template 函式不變) ...


# app_name/utils/f.py

# ... (保持匯入不變) ...

# ... (保持 API_ENDPOINT_URL 不變) ...

# ... (保持其他函式不變) ...


def query_image(work_id: str, text: str, query_count: int) -> dict:
    """
    呼叫外部 API 查詢圖片相關資訊 (image_base64_text, score, content)。

    :param work_id: 工作的 ID。
    :param text: 額外的文字描述或查詢。
    :param query_count: 查詢的數量 (預期範圍 1~5)。
    :return: 包含 status, data, message 的字典。
    """
    
    # 參數檢查 (確保 query_count 在 1~5 範圍內)
    if not (1 <= query_count <= 25):
        return {
            'status': 'error', 
            'message': f'query_count 必須在 1 到 25 之間，但收到了 {query_count}',
            'api_status_code': 400
        }
    
    data = {
        'work_id': work_id,
        'text': text,
        # 關鍵變動：新增 query_count 參數
        'query_count': query_count,
        'key': QUERY_KEY
    }
    
    try:
        # 發送 GET 請求
        api_response = requests.get(API_ENDPOINT_URL, data=data, timeout=10) 
        
        # 檢查 API 狀態碼
        api_response.raise_for_status() 
        
        api_data = api_response.json()
        
        if api_data.get('status') == 'success' and 'data' in api_data:
            return api_data
        else:
            return {
                'status': 'error', 
                'message': api_data.get('message', 'API returned success status but missing data or internal error.'),
                'api_status_code': api_response.status_code
            }

    except requests.exceptions.HTTPError as http_err:
        return {
            'status': 'error', 
            'message': f'API HTTP Error: {http_err}', 
            'api_status_code': api_response.status_code
        }
    except requests.exceptions.RequestException as req_err:
        return {
            'status': 'error', 
            'message': f'API Connection Error: {req_err}', 
            'api_status_code': None
        }
    except json.JSONDecodeError:
        return {
            'status': 'error', 
            'message': 'API returned invalid JSON response',
            'api_status_code': api_response.status_code if 'api_response' in locals() else None
        }