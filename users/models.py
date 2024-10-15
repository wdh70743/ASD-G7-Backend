from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, verbose_name='username')
    email = models.EmailField(verbose_name='email', unique=True)
    password = models.CharField(max_length=1000, verbose_name='password')
    note = models.TextField(verbose_name='note', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')

    def __str__(self):
        return self.email



