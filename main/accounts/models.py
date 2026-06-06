from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for students."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    is_lecturer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({'Lecturer' if self.is_lecturer else 'Student'})"

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username
