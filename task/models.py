from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('To-Do', 'To-Do'),
        ('In-Progress', 'In-Progress'),
        ('Review', 'Review'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To-Do')
    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
