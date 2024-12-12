from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import News, FavoriteNews

# Отображение списка всех новостей
def news_list(request):
    news = News.objects.all()  # Получение всех новостей
    return render(request, 'news_list.html', {'news': news})

# Добавление новости в избранное
@login_required
def add_to_favorites(request, news_id):
    news_item = News.objects.get(id=news_id)  # Получаем новость по ID
    FavoriteNews.objects.get_or_create(user=request.user, news=news_item)  # Добавляем в избранное
    return redirect('news_list')

# Отображение списка избранных новостей
@login_required
def favorite_news(request):
    favorites = FavoriteNews.objects.filter(user=request.user)  # Избранное для текущего пользователя
    return render(request, 'favorite_news.html', {'favorites': favorites})
