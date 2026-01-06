from django.urls import path
from . import views

# 為了命名空間 (Namespace) 區隔，這是最佳實踐
app_name = 'myapp' 

'''
urlpatterns = [
    path('', views.home, name='home'),
    # 當專案urls.py轉發 'hello/' 過來時，這會匹配到
    path('upload-image/', views.upload_image_to_webhook, name='upload_image'),
    path('upload/', views.upload_form_view, name='upload_form'),
    path('query-image/', views.query_image_view, name='query_image'),
    # # 當專案urls.py轉發 'about/' 過來時，這會匹配到
    # path('about/', views.about_page, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search-scene/', views.search_scene, name='search_scene'),
    #path('register/', views.user_register, name='register'),
]
'''

urlpatterns = [
    # 1. 主頁
    path('', views.home, name='home'),
    
    # 2. 查詢圖片頁面 (包含頁面渲染與 API 搜尋)
    path('query/', views.query_image_view, name='query_image'),
    # 建議新增一個專門回傳 JSON 的 API 路徑，供前端 JavaScript 呼叫
    path('api/search/', views.search_scene_api, name='search_scene_api'),
    path('api/search/', views.search_api, name='search_api'),
    
    # 3. 上傳圖片
    path('upload/', views.upload_form_view, name='upload_form'),
    
    # 4. 帳戶相關
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 如果之後要啟用註冊，取消下面這行註解
    path('register/', views.register_view, name='register'),
    
    # 5. 圖片上傳到 n8n Webhook 的功能性 API
    path('upload-image/', views.upload_image_to_webhook, name='upload_image'),



]