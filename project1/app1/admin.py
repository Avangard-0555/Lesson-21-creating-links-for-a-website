from django.contrib import admin
from .models import News, FavoriteNews

admin.site.register(News)         # Регистрируем модель новостей
admin.site.register(FavoriteNews) # Регистрируем модель избранного
