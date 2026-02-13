from django.contrib import admin
from .models import Category, Note

# Category と Note を管理画面で操作可能にする
admin.site.register(Category)
admin.site.register(Note)
