"""MyDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from .settings import DEBUG, MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 将sixi应用下的所有路由导入到工程路由总路由入口文件
    url(r'^', include(('sixi.urls', 'sixi'), namespace='sixi')),
    #富文本编辑器
    url(r'ckeditor/', include('ckeditor_uploader.urls')),

    #评论
    url(r'comment/', include(('comment.urls','comment'),namespace='comment')),
]

if DEBUG:
    urlpatterns+=url(r'^media/(?P<path>.*)/$',serve,{'document_root':MEDIA_ROOT}),
