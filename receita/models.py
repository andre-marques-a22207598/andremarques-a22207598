from django.db import models

# Create your models here.
from django.db import models

class Receita(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField()
    tempo_preparo = models.IntegerField(help_text="Tempo em minutos")

    def __str__(self):
        return self.nome
