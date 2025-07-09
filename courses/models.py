from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from online_learning import settings

class Course(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"