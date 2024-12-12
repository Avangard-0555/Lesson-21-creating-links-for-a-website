from django.db import models
from django.contrib.auth.models import User

# Модель новостей
class News(models.Model):
    title = models.CharField(max_length=200)  # Заголовок новости
    content = models.TextField()             # Текст новости
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title

# Модель для избранных новостей
class FavoriteNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь
    news = models.ForeignKey(News, on_delete=models.CASCADE)  # Связанная новость

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"
