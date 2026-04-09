from django.db import models

# Create your models here.

class Owner(models.Model):
    nome = models.CharField(max_length=100)
    bio = models.TextField()
    foto = models.ImageField(upload_to='perfil/')
    email = models.EmailField()
    github = models.URLField()
    linkedin = models.URLField()
    cv = models.FileField(upload_to='cv/')

