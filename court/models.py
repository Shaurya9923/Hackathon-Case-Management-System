from django.db import models

# Create your models here.

class Court_Type(models.Model):
    name = models.CharField(max_length=50,unique=True)
    parent_court = models.ForeignKey("self", on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s' % (self.name)
    
class Court(models.Model):
    court_type = models.ForeignKey(Court_Type,on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    address=models.TextField(null=True)
    contact_no = models.CharField(max_length=10,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s of %s' % (self.court_type,self.place)

class Practice_Area(models.Model):
    name=models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s' % (self.name)
    