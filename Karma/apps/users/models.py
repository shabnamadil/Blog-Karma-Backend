from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email

from .manager.user_manager import UserManager


class User(AbstractUser):
    first_name = models.CharField('Ad', max_length=150)
    last_name = models.CharField('Soyad', max_length=150)
    email = models.EmailField(unique=True, validators=(validate_email,))
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password',]
    objects = UserManager()

    def __str__(self) -> str:
        if self.get_full_name():
            return self.get_full_name()
        else:
            return "Admin User"
       
    @property
    def user_full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return "Admin User"
        

class Profile(models.Model):
    image = models.ImageField(
        'Foto',
        upload_to='user-images', 
        null=True, blank=True
    )
    bio = models.TextField(
        'İstifadəçi haqqında qısa məlumat',
        max_length=500
    )
    profession = models.CharField(
        'Peşə',
        max_length=255, 
        null=True, blank=True
    )
    mobile_number = models.CharField(
        'Əlaqə nömrəsi',
        max_length=20, 
        help_text='Only numeric values allowed', 
        null=True, blank=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, 
        related_name="user_profile"
    )

    def __str__(self) -> str:
        return f'{self.user} profile'
