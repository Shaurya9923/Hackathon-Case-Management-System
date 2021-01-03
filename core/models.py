from django.db import models
from django.contrib.auth.models import AbstractUser
from organization.models import organization,department

# Create your models here.
class User(AbstractUser):
    middle_name = models.CharField(max_length=30)
    ref_user = models.ForeignKey("self", on_delete=models.CASCADE,null=True,blank=True)
    org = models.ForeignKey(organization,on_delete=models.CASCADE,null=True)
    dept = models.ForeignKey(department,on_delete=models.CASCADE,null=True,blank=True) 
    contact_no = models.CharField(max_length=10,null=True,blank=True)

    nodal_officer="nodal_officer"
    head = "head_of_the_department"
    superadmin="super_admin"

    role_choice = ((nodal_officer,'nodal_officer'),(head,'head_of_the_department')
    ,(superadmin,'super_admin'))

    role = models.CharField(max_length=35,choices=role_choice,default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        if type(self.org)!=type(None):
            return '%s at %s' % (self.username,self.org.name)
        else:
            return '%s' % (self.username)