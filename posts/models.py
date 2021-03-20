from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
User = get_user_model()


class Group(models.Model):
    """Модель группы"""
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    """Модель поста"""
    text = models.TextField('Текст', help_text='Введите содержимое поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Группа',
                              help_text='Выберите группу, к которой относится пост')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение',
                              help_text='Загрузите изображение')

    def __str__(self):
        return self.text[:15]

    def get_absolute_url(self):
        return reverse('post', kwargs={'username': self.author.username, 'id': self.id})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Модель коммпентария"""
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', verbose_name='Пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='Автор')

    def __str__(self):
        return self.user.username + '-' + self.author.username

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подсписки'


