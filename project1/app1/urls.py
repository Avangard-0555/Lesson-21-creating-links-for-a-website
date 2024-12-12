from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),  # Список новостей
    path('news/add-to-favorites/<int:news_id>/', views.add_to_favorites, name='add_to_favorites'),  # Добавить в избранное
    path('favorites/', views.favorite_news, name='favorite_news'),  # Избранное
]
