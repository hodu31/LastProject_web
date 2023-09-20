
from django.contrib import admin
from django.urls import path, include

### firstapp 폴더 하위에 있는 views.py 파일 읽어들이기
# - 라이브러리 읽어들이는 것과 동일
from . import views

"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
# - http://127.0.0.1:8000/main/ 
    path('', views.index),
    
# - INDEX 페이지 2~3
    path('index_2/', views.index2),
    path('index_3/', views.index3),
    
    
### 로그인 처리
    path('login_chk/', views.login_chk), 
    path('login/', views.login_pg), 
### 로그아웃 처리
    path('logout_chk/', views.logout_chk),

]
