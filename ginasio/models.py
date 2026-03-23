from django.db import models

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    plano = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
