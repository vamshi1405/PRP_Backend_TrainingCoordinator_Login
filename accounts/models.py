from django.db import models
from django.contrib.auth.models import User


class TrainingCoordinator(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="training_coordinator"
    )
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name