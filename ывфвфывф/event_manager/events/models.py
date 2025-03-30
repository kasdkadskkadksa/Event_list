from django.db import models
from django.core.validators import EmailValidator

class Event(models.Model):
    STATUS_CHOICES = [
        ('PL', 'Запланировано'),
        ('IP', 'В процессе'),
        ('CO', 'Завершено'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"