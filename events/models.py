from django.db import models
from django.core.validators import EmailValidator

class Event(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    start_date = models.DateTimeField(verbose_name='Дата и время начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания')
    location = models.CharField(max_length=200, verbose_name='Локация')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Participant(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name='Электронная почта')  # Убрано unique=True
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['email', 'event']  # Уникальность email в рамках одного события

    def __str__(self):
        return f"{self.name} ({self.email})"
# #class Participant(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Имя')
#     email = models.EmailField(
#         unique=True,
#         validators=[EmailValidator()],
#         verbose_name='Электронная почта'
#     )
#     event = models.ForeignKey(
#         Event,
#         on_delete=models.CASCADE,
#         related_name='participants',
#         verbose_name='Событие'
#     )
#     registration_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.name} ({self.email})"#