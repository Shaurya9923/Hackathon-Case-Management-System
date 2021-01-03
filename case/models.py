from django.db import models
from core.models import User
from court.models import Court,Court_Type,Practice_Area
# Create your models here.

class lawyers(models.Model):

    first_name= models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=10,null=True)
    email = models.CharField(max_length=50)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s' % (self.first_name)

class user_lawyer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lawyer = models.ForeignKey(lawyers,on_delete=models.CASCADE)



class cases(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    court = models.ForeignKey(Court,on_delete=models.CASCADE)
    type = models.ForeignKey(Practice_Area,on_delete=models.CASCADE)
    case_number = models.CharField(max_length=100,null=True,unique=True)
    case_priority = models.IntegerField(null=True)

    case_reminder = models.IntegerField(default=7,null=True)

    title = models.CharField(max_length=50)
    
    detail_doc = models.FileField(upload_to='documents/cases',null=True)

    admission='ADMISSION'
    allocated='ALLOCATED'
    approved ='APPROVED'
    rejected='REJECTED'    
    responded='RESPONDED'
    initiated='INITIATED'
    process='PROCESS'
    judgement='JUDGEMENT'

    status_choice = ((admission,'ADMISSION'),(allocated,'ALLOCATED'),(approved,'APPROVED'),('REJECTED','REJECTED'),('RESPONDED','RESPONDED')
    ,(initiated,'INITIATED'),(process,'PROCESS'),(judgement,'JUDGEMENT'))
    status = models.CharField(max_length=15,choices=status_choice,null=True)

    opponent_name = models.CharField(max_length=50,null=True)
    opponent_contact_no = models.CharField(max_length=10,null=True)
    opponent_email = models.CharField(max_length=50,null=True)
    opponent_address = models.TextField(null=True)

    next_hearing_at = models.DateField(null=True)

    reply = models.FileField(upload_to='documents/reply',null=True,blank=True)
    rejoinder = models.FileField(upload_to='documents/rejoinder',null=True,blank=True)
    
    case_synopsis= models.TextField(null=True,blank=True)
    action_taken= models.TextField(null=True,blank=True)    

    judgement_at = models.DateField(null=True)
    

    pending= 'pending'
    won='won'
    defeat = 'defeat'

    result_choice = ((pending,'pending'),(won,'won'),(defeat,'defeat'))

    decision_sought = models.CharField(max_length=15,choices=result_choice,null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    decision = models.TextField(null=True,blank=True)

    def __str__(self):
        return '%s vs %s' % (self.user,self.opponent_name)

class case_lawyers(models.Model):
    case = models.ForeignKey(cases,on_delete=models.CASCADE)
    lawyer = models.ForeignKey(lawyers,on_delete=models.CASCADE)

    admission='ADMISSION'
    allocated='ALLOCATED'
    approved ='APPROVED'
    rejected='REJECTED'    
    responded='RESPONDED'
    initiated='INITIATED'
    process='PROCESS'
    judgement='JUDGEMENT'

    status_choice = ((admission,'ADMISSION'),(allocated,'ALLOCATED'),(approved,'APPROVED'),('REJECTED','REJECTED'),('RESPONDED','RESPONDED')
    ,(initiated,'INITIATED'),(process,'PROCESS'),(judgement,'JUDGEMENT'))
    status = models.CharField(max_length=15,choices=status_choice,null=True)


    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s' % (self.lawyer)
    
class case_hearings(models.Model):
    case = models.ForeignKey(cases,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hearing_at=models.DateField()
    prev_hearing = models.ForeignKey("self", on_delete=models.CASCADE,null=True,blank=True)
    description=models.TextField()
    detail_doc = models.FileField(upload_to='documents/hearings',null=True)
    Interim='Interim'
    Final= 'Final'
    
    status_choice=((Interim,'Interim'),(Final,'Final'))

    order_type= models.CharField(max_length=15,choices=status_choice,null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s at %s' % (self.case,self.hearing_at)

class case_invoices(models.Model):
    case = models.ForeignKey(cases,on_delete=models.SET_NULL,null=True)
    hearing = models.ForeignKey(case_hearings,on_delete=models.CASCADE)
    
    taxable_total=models.FloatField(null=True,default=0.0)
    gst = models.FloatField(null=True,default=0.0)
    invoice_doc = models.FileField(upload_to='documents/invoices',null=True)
    unpaid='UNPAID'
    paid='PAID'
    status_choice=((unpaid,'UNPAID'),(paid,'PAID'))
    payment_status = models.CharField(max_length=15,choices=status_choice,null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '%s vs %s' % (self.case,self.hearing)


class log_table(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    lawyer = models.ForeignKey(lawyers,on_delete=models.CASCADE,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)