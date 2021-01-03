from django.shortcuts import render,redirect
from .models import User
from organization.models import organization,department
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import auth
from case.models import log_table

# Create your views here.
import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core import mail


def signup(request):
    
    if request.method=='POST':
        first_name = request.POST.get('firstName')
        middle_name = request.POST.get('middleName')
        last_name = request.POST.get('lastName')
        email=request.POST.get('emailId').lower()
        password=request.POST.get('password')
        contact_no=request.POST.get('contactNumber')
        org_name=request.POST.get('companyName').lower()
        dept_name=request.POST.get('department').lower()
        address=request.POST.get('address').lower()
        city= request.POST.get('city').lower()

        # this is for Organization exist  or not exist and add

        if organization.objects.filter(name=org_name).exists():
            # print("if organization already there")
            org = organization.objects.filter(name=org_name)

            # print(org.city,type(org.city))

            for i in org:            
                if i.city == city:
                    # print("if City is Same ")
                    try:
                        if i.address == address:
                            org = organization.objects.filter(name=org_name,address=address,city=i.city)[:1].get()
                        else:
                            org = organization.objects.create(name=org_name,address=address,city=city) 
                    except:
                        org = organization.objects.filter(name=org_name,address=address,city=i.city)[:1].get()
                else:
                    # print("if City is not Same ")
                    org = organization.objects.create(name=org_name,address=address,city=city) 
                             

            # print(org,org.pk)

        else:    
            # print("if organization New")
            org = organization.objects.create(name=org_name,address=address,city=city)

            # print(org,org.pk)

        # this is for Department exist  or not exist and add

        if dept_name != "":
            
            if department.objects.filter(name=dept_name).exists():
                
               dept = department.objects.filter(name=dept_name)

               for i in dept:
                #    print(i.name,"at",i.org.name)
                   try:
                       if org.name==i.org.name:
                           dept = department.objects.filter(org=i.org,name=dept_name)[:1].get()
                       else:
                          dept = department.objects.create(name=dept_name,org=org)
                   except:
                        # print("Catch")
                        dept = department.objects.filter(org=i.org,name=dept_name)[:1].get()

            else:
                # print("Department is not same")
                dept = department.objects.create(name=dept_name,org=org)
            

        else:
            dept=None

        if User.objects.filter(first_name=first_name,middle_name=middle_name,last_name=last_name,org=org,dept=dept,role=User.nodal_officer).exists():

            return render(request,'Login/login.html')

        else:
            num = random.randint(1000,10000)
            name=first_name+str(num)

            while User.objects.filter(username=num).exists():
                num = random.randint(1000,10000) 
                name=first_name+str(num)

            user =User.objects.create_user(username=name,first_name=first_name,middle_name=middle_name,last_name=last_name,email=email,password=password,contact_no=contact_no,org=org,dept=dept,role=User.nodal_officer)   
            user.save()
            
        
        # print(user.username)
        
        
        html_content = render_to_string("notification/email_template.html",{'title':'test email','content':'Hello '+str(user.first_name)+" Your User name is "+str(user.username)+"\n and your password is :"+str(password)})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            #subject
            "SignupSuccessFul",
            #content
            text_content,
            #from email
            settings.EMAIL_HOST_USER,
            # rec list
            [user.email]
        )

        
        email.attach_alternative(html_content,"text/html")
        email.send()
                
        return render(request,'Login/login.html')

    else:

        return render(request,'Signup/signup.html')

def login(request):

    if request.method=='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('loginPassword')

        # print(username,password)

        user = auth.authenticate(username=username,password=password)   # check that user is availabe in 'auth_user' table or not

        if user is not None:    #if available
            auth.login(request,user)     # activate the login

            # print(user.role)

            if user.role==User.superadmin:

                return render(request,'SuperAdmin/Dashboard.html',{'user':user.pk})

            elif user.ref_user is not None:

                if user.role == User.nodal_officer:
                    
                    # return redirect('/nodaldashboard/'+str(user.pk))
                    return render(request,'Dashboard/nodal_officer/Dashboard.html',{'user':user.pk})
                elif user.role == User.head:
                    # return redirect('/nodaldashboard/'+str(user.pk))
                    user_h = User.objects.get(username=username)

                    print(user_h.pk)

                return render(request,'HeadDashboard/Dashboard.html',{'user':user_h.pk})
            else:
                messages.info(request,"You are not authorized person!!")

                return render(request,'Login/login.html')
            
            
        else:

            messages.info(request,"Sorry :( Something Went Wrong !!")

            return render(request,'Login/login.html')
    
    else:

        return render(request,'Login/login.html')

def logout(request):

    auth.logout(request)
    return render(request,'Login/login.html')

def requestlog(request,userid):

    user_without_ref = User.objects.filter(ref_user=None)

    without_ref=[]

    for i in user_without_ref:
        if i.role==User.nodal_officer:
            without_ref.append(i)
    

    return render(request,'SuperAdmin/Request.html',{'user':userid,'nodal':without_ref})

def do_accept(request,userid,refid):

    user = User.objects.get(pk=userid)

    print(user)

    user.ref_user = User.objects.get(pk=refid)

    user.save()

    log_table.objects.create(user=user)

    return redirect('/requestlog/'+str(refid))

def do_reject(request,userid,refid):

    user = User.objects.get(pk=userid)

    print(user)

    user.delete()

    return redirect('/requestlog/'+str(refid))


