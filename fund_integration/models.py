from django.db import models

# Create your models here.
from django.db import models

class MutualFund(models.Model):
    scheme_code = models.IntegerField()
    scheme_name = models.CharField(max_length=255)

    def __str__(self):
        return self.scheme_name
