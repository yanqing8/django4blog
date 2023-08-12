"""
URL configuration for django4blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf.urls.static import static
import article.views
import comment.views
import userprofile.views
from django4blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 添加app的url
    path('hello/', article.views.hello),
    re_path(r'^$', article.views.article_list),
    path('list/', article.views.article_list, name='list'),  # 文章列表
    path('detail/<int:id>/', article.views.article_detail, name='detail'),  # 文章详情
    path('create/', article.views.article_create, name='create'),  # 文章创建
    path('delete/<int:id>/', article.views.article_delete, name='delete'),  # 文章删除
    path('update/<int:id>/', article.views.article_update, name='update'),  # 文章更新

    path('login/', userprofile.views.user_login, name='login'),
    path('logout/', userprofile.views.user_logout, name='logout'),
    path('register/', userprofile.views.user_register, name='register'),

    path('post-comment/<int:article_id>/', comment.views.post_comment, name='post_comment'),

    path('mdeditor/', include('mdeditor.urls')),
    path('upload/', article.views.upload, name='upload')
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)主要是让页面显示正常
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
