from django.contrib import admin

from .models import IP, Blog, Category, Comment

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
