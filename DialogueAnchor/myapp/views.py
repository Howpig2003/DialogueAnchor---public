# project_name/app_name/views.py

import json
import requests, os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # 根據需要決定是否使用
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .utils.query_image import query_image
from .utils.get_work_list import get_all_works_json_for_template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

# 替換成您的 Webhook URL
WEBHOOK_URL = os.environ.get('api_upload_url', 'https://example.com/webhook')
UPLOAD_KEY = os.environ.get('upload_key', 'your-upload-key') 

   
# test data
def get_work_list():
    """模擬作品清單，之後可改為從資料庫讀取"""
    '''
    return [
        {"id": 1, "title": "重慶森林"},
        {"id": 2, "title": "大話西遊"},
        {"id": 3, "title": "黑暗騎士"}
    ]
    '''
    #print(type(get_all_works_json_for_template()))
    #print(json.loads(get_all_works_json_for_template())[0])
    data = json.loads(get_all_works_json_for_template())

    # 使用列表推導式重新構造字典
    new_data = [
        {'id': item['id'], 'title': item['work_name']} 
        for item in data
    ]

    #print(new_data)
    return new_data

def home(request):
    """首頁介紹"""
    return render(request, 'core/home.html')

def query_image_view(request):
    """查詢圖片頁面 (渲染畫面)"""
    context = {'work_list': get_work_list()}
    return render(request, 'core/query_image.html', context)


@login_required(login_url='myapp:login')
def upload_form_view(request):
    """上傳圖片頁面 (渲染畫面)"""
    context = {'work_list': get_work_list()}
    return render(request, 'core/upload_form.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('myapp:home')  # 登入成功跳轉至查詢頁面
        else:
            messages.error(request, "帳號或密碼錯誤")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# 註冊功能
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # 註冊完自動登入
            messages.success(request, "註冊成功！")
            return redirect('myapp:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# 登出功能
def logout_view(request):
    logout(request)
    return redirect('myapp:login')
'''
def login_view(request):
    """登入頁面"""
    return render(request, 'core/login.html')

def logout_view(request):
    """執行登出並導向首頁"""
    logout(request)
    return redirect('myapp:home')
'''

'''
@login_required # 關鍵：確保只有登入者能訪問
def upload_scene(request):
    if request.method == 'POST':
        # 處理圖片和資訊，request.FILES 是用來處理檔案上傳的
        form = SceneUploadForm(request.POST, request.FILES)
        if form.is_valid():
            scene = form.save(commit=False)
            scene.uploaded_by = request.user # 記錄上傳者
            scene.save()
            
            # TODO: 這裡將來是呼叫 n8n Webhook 的位置
            # 目前先印出 DEBUG 訊息，並導向首頁
            print(f"DEBUG: 場景已儲存: {scene.work_title}, 準備呼叫 n8n 處理: {scene.image.path}")
            return redirect('home') 
    else:
        # 顯示空表單 (GET 請求)
        form = SceneUploadForm()
        
    context = {'form': form}
    return render(request, 'core/upload_scene.html', context)
'''
'''
def login_view(request):
    """處理使用者登入的視圖函式 (待實作)"""
    return HttpResponse("Login view - 待實作")

def logout_view(request):
    """處理使用者登出的視圖函式 (待實作)"""
    return HttpResponse("Logout view - 待實作")
'''


# --- 2. 功能性 API (處理邏輯) ---
'''
@require_http_methods(["GET"]) 
def search_scene_api(request):
    """
    接收 work_id, text, query_count 參數，回傳搜尋結果 JSON。
    對應 URL: /api/search/
    """
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    query_count = request.GET.get('query_count', '1')

    if not work_id or not user_text:
        return JsonResponse({'status': 'error', 'message': '缺少作品 ID 或查詢文字'}, status=400)

    # 呼叫你原本寫好的 utils 中的 query_image 函數
    from .utils.query_image import query_image
    api_result = query_image(work_id=work_id, text=user_text, query_count=int(query_count))
    
    return JsonResponse(api_result, status=200 if api_result.get('status') == 'success' else 500)
'''
@require_http_methods(["GET"]) 
def search_scene_api(request):
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    query_count_str = request.GET.get('query_count', '3')

    # 1. 型別轉換
    try:
        query_count = int(query_count_str)
    except ValueError:
        query_count = 3

    # 2. 呼叫服務函式
    api_result = query_image(work_id=work_id, text=user_text, query_count=query_count)
    
    
    # 3. 判斷並列印多筆邏輯
    if api_result.get('status') == 'success':
        data = api_result.get('data', [])
        
        # 根據你提供的檔案，data 是一個陣列
        if isinstance(data, list):
            print(f"--- [成功] 檢索到 {len(data)} 筆場景 ---")
            for i, item in enumerate(data):
                # 這裡處理 image_base64_text 是陣列的情況
                score = item.get('score')
                content = item.get('content')[:20] # 只印前20字
                print(f"    結果 {i+1}: 分數={score}, 內容={content}...")
        
        return JsonResponse(api_result)
    else:
        status_code = api_result.get('api_status_code')
        http_status = status_code if status_code and 400 <= status_code < 600 else 500
        return JsonResponse(api_result, status=http_status)
'''
@require_http_methods(["GET"]) 
def search_scene_api(request):
    """
    接收前端 fetch 請求，呼叫外部 API 查詢場景。
    URL: /api/search/?work_id=...&text=...&query_count=...
    """
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    query_count_str = request.GET.get('query_count', '3')
    print(f'Received search_scene_api request: work_id={work_id}, text={user_text}, query_count={query_count_str}')

    # 1. 參數檢查
    if not work_id or not user_text:
        return JsonResponse({'status': 'error', 'message': '缺少作品 ID 或查詢文字'}, status=400)

    # 2. 型別轉換與範圍處理
    try:
        query_count = int(query_count_str)
    except ValueError:
        query_count = 3

    # 3. 呼叫服務函式 (此時 utils/query_image.py 內的 URL 應已更新)
    api_result = query_image(work_id=work_id, text=user_text, query_count=query_count)
    
    # 4. 判斷回傳結果
    if api_result.get('status') == 'success':
        results = api_result.get('data', [])
        # 判斷 data 是單一字典還是清單
        count = len(results) if isinstance(results, list) else 1
        print(f"--- 搜尋成功：回傳了 {count} 筆場景資料 ---")
        return JsonResponse(api_result)
    else:
        # 決定錯誤狀態碼
        status_code = api_result.get('api_status_code')
        http_status = status_code if status_code and 400 <= status_code < 600 else 500
        return JsonResponse(api_result, status=http_status)
'''


@require_http_methods(["GET"]) 
def search_api(request):
    """處理前端傳來的搜尋請求並列印參數"""
    
    # 1. 接收參數
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    raw_query_count = request.GET.get('query_count', '1')

    # 2. 安全轉型 query_count
    try:
        query_count = int(raw_query_count)
        # 限制範圍在 1~5 之間
        query_count = max(1, min(5, query_count))
    except (ValueError, TypeError):
        query_count = 1  # 若轉型失敗則預設為 1

    # 3. 在終端機列印 (便於觀察是否為多筆)
    print(f"\n[API 請求] 作品:{work_id} | 數量:{query_count} | 內容: {user_text}")

    # 4. 執行查詢
    try:
        result = query_image(
            work_id=work_id, 
            text=user_text, 
            query_count=query_count
        )
        
        # 觀察回傳的資料結構 (若是多筆，result['data'] 應該是 list)
        if result.get('status') == 'success':
            data_payload = result.get('data', [])
            result_size = len(data_payload) if isinstance(data_payload, list) else 1
            print(f"[API 成功] 回傳了 {result_size} 筆場景資料")
            
        return JsonResponse(result)

    except Exception as e:
        print(f"[API 錯誤]: {e}")
        return JsonResponse({'status': 'error', 'message': '伺服器內部錯誤'}, status=500)
'''
def search_api(request):
    """處理前端傳來的搜尋請求並列印參數"""
    
    # 1. 使用 request.GET.get('key') 接收參數
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    query_count = request.GET.get('query_count', '1') # 預設值為 '1'

    # 2. 在終端機 (Terminal) 中 Print 出來
    print("\n--- 收到搜尋請求 ---")
    print(f"作品 ID (work_id): {work_id}")
    print(f"台詞內容 (text): {user_text}")
    print(f"查詢數量 (query_count): {query_count}")
    print("-------------------\n")

    # 3. 呼叫你的 utils 邏輯並回傳
    try:
        result = query_image(
            work_id=work_id, 
            text=user_text, 
            query_count=int(query_count)
        )
        return JsonResponse(result)
    except Exception as e:
        print(f"錯誤: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

'''

'''
@require_http_methods(["POST"]) 
def upload_image_to_webhook(request):
    """處理圖片上傳至 n8n Webhook"""
    work_id = request.POST.get('work_id')
    if 'image_file' not in request.FILES or not work_id:
        return JsonResponse({'error': '資料不完整'}, status=400)

    uploaded_file = request.FILES['image_file']
    files = {'image': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)}
    data = {'work_id': work_id, 'key': UPLOAD_KEY}
    
    try:
        response = requests.post(WEBHOOK_URL, data=data, files=files, timeout=30)
        return JsonResponse({'message': '上傳成功', 'status': response.status_code})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
'''

# Howpig

def search_scene(request):
    """
    處理文字查詢場景的 View (待實作 n8n 呼叫)
    目前只會渲染首頁，並在未來顯示結果
    """
    
    # 從 URL 參數中獲取查詢關鍵字 (e.g., ?query=台詞)
    query = request.GET.get('query')
    
    # TODO: 這裡將來會是呼叫 n8n 向量搜尋的核心邏輯
    
    context = {
        'query': query,
        # 暫時回傳空的結果列表，避免模板報錯
        'search_results': [], 
    }
    
    # 這裡我們將其渲染回首頁，但可以視需求渲染到一個獨立的 search.html 頁面
    return render(request, 'core/home.html', context)






# 假設您只需要處理 POST 請求
# @csrf_exempt 
@login_required(login_url='myapp:login')
@require_http_methods(["POST"]) 
def upload_image_to_webhook(request):
    """
    處理圖片上傳，並將二進制圖片檔案和 work_id 發送到 Webhook。
    """
    if request.method == 'POST':
        # 1. 檢查 work_id 是否存在
        work_id = request.POST.get('work_id')
        if not work_id:
            return JsonResponse({'error': 'Missing work_id in POST data'}, status=400)

        # 2. 檢查是否有圖片檔案
        if 'image_file' not in request.FILES:
            return JsonResponse({'error': 'Missing image_file in uploaded files'}, status=400)
        
        uploaded_file = request.FILES['image_file']
        
        # 3. 準備發送到 Webhook 的數據
        
        # 檔案數據: 'image': (檔案名稱, 檔案的二進制內容, 內容類型)
        # 這裡我們使用檔案的 read() 方法獲取完整的二進制內容
        files = {
            'image': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        }
        
        # 額外數據 (work_id)
        data = {
            'work_id': work_id,
            'key': UPLOAD_KEY
        }
        
        try:
            # 4. 發送 POST 請求到 Webhook
            # requests 會自動處理 multipart/form-data 格式
            webhook_response = requests.post(WEBHOOK_URL, data=data, files=files, timeout=30)
            
            # 5. 處理 Webhook 的回覆
            if webhook_response.status_code == 200:
                # Webhook 成功接收
                return JsonResponse({
                    'message': 'Image and work_id successfully sent to webhook.',
                    'webhook_status': webhook_response.status_code,
                    # 您可以根據需要返回 Webhook 的回應內容
                    # 'webhook_data': webhook_response.json() 
                })
            else:
                # Webhook 返回錯誤
                return JsonResponse({
                    'message': f'Webhook failed with status code {webhook_response.status_code}',
                    'webhook_status': webhook_response.status_code,
                    'webhook_text': webhook_response.text
                }, status=502) # 502 Bad Gateway 常用於表示外部服務錯誤
                
        except requests.exceptions.RequestException as e:
            # 請求發送過程中出錯 (例如網路連線問題)
            return JsonResponse({'error': f'Failed to connect to webhook: {e}'}, status=500)
        
    # 如果不是 POST 請求，則返回方法不允許
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 提示: 如果您不使用 @csrf_exempt，請確保前端在發送 POST 請求時包含 CSRF token。
# 或者，如果您只允許 API 存取，可以考慮使用 Django Rest Framework (DRF) 
# 並設定適當的權限和驗證。
'''
@require_http_methods(["GET"]) 
def upload_form_view(request):
    """
    渲染包含上傳表單的 HTML 模板。
    """
    return render(request, 'upload_form.html')
'''



'''
# 視圖函式：處理圖片查詢請求
@require_http_methods(["GET"]) 
def query_image_view(request):
    """
    視圖函式：接收 work_id, text, query_count 參數，呼叫 query_image 服務函式。
    """
    
    # 1. 獲取 URL 查詢參數
    work_id = request.GET.get('work_id')
    user_text = request.GET.get('text')
    # 獲取 query_count，並嘗試轉換為整數 (預設值為 1)
    query_count_str = request.GET.get('query_count', '1') 
    
    # 2. 基本參數檢查
    if not work_id or not user_text:
        return JsonResponse(
            {'status': 'error', 'message': 'Missing work_id or text in query parameters'}, 
            status=400
        )
        
    # 3. query_count 類型與範圍檢查
    try:
        query_count = int(query_count_str)
    except ValueError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid query_count format. Must be an integer.'}, 
            status=400
        )

    # 4. 呼叫服務函式
    # ⚠️ 這裡不需要再次檢查 1~5 範圍，因為 query_image 函式內部已經處理了這個邏輯
    api_result = query_image(
        work_id=work_id, 
        text=user_text, 
        query_count=query_count # 傳遞新的參數
    )
    
    # 5. 根據服務函式的結果回傳 JSON 響應
    
    # 如果函式內部因為 query_count 範圍錯誤而返回 error，這裡會被捕捉
    if api_result.get('status') == 'success':
        return JsonResponse(api_result)
    else:
        status_code = api_result.get('api_status_code')
        
        if status_code and 400 <= status_code < 600:
            http_status = status_code 
        elif status_code is None:
             http_status = 500 
        else:
            http_status = 502 
            
        return JsonResponse(api_result, status=http_status)
'''