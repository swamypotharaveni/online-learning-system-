from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
class UserProfile(AbstractUser):
    is_student=models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    
    def __str__(self):
        return self.username

