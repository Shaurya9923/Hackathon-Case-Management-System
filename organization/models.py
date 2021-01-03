from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class organization(models.Model):
    name=models.CharField(max_length=50)
    address=models.TextField()
    city = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s at %s' % (self.name,self.city)
    class Meta:
        unique_together=('name','address','city')

class department(models.Model):

    name=models.CharField(max_length=20)
    org = models.ForeignKey(organization,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s %s' % (self.name,self.org)
    
    class Meta:
        unique_together=('name','org')


