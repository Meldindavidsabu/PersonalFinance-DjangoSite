from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    bill_number = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='documents/')
    
    def __str__(self):
        return self.title
