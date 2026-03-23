from django.db import models

# Create your models here.
from django.db import models

class Festival(models.Model):
    nome = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    data = models.DateField()

    def __str__(self):
        return self.nome
