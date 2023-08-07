from django.contrib import admin

# Register your models here.
# 导入Article
from .models import Article

# 注册Article到admin中。如果有多个模型，在模型后面用 ,隔开
admin.site.register(Article)
