from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]
    
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    content = models.TextField('Содержание')
    excerpt = models.TextField('Краткое описание', max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)  # ← ВРЕМЕННО
    image = models.ImageField('Изображение', upload_to='blog/%Y/%m/', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True, null=True, blank=True)  # ← ВРЕМЕННО
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    published_at = models.DateTimeField('Опубликовано', default=timezone.now, null=True, blank=True)  # ← ВРЕМЕННО
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('Просмотры', default=0)
    meta_title = models.CharField('Meta title', max_length=200, blank=True)
    meta_description = models.TextField('Meta description', max_length=300, blank=True)
    
    # Связь с товарами для рекомендаций
    related_products = models.ManyToManyField('catalog.Product', blank=True, verbose_name='Связанные товары')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField('Комментарий', max_length=1000)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    is_approved = models.BooleanField('Одобрен', default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Комментарий {self.author} к "{self.article}"'