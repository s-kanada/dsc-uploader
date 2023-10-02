"""
mysiteのurls.pyから拡張、こっちに記載
httpリクエストでアクセスしたURLに対応するviewを振分け
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from .views.upload_file import upload_file
from .views.register import register

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', register, name='register'),
    path('upload/', upload_file, name='upload_file'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # その他のURLパターンを追加することができます
]
