from django.shortcuts import render,redirect
from core.models import User
from .models import organization,department
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from case.models import lawyers,user_lawyer,case_lawyers,cases,log_table,case_hearings
# Create your views here.

import random

@login_required(login_url='/login/')
def nodaldashboard(request,userid):

    # print(userid)

    user = User.objects.get(pk=userid)

    # print(user.pk,user.role)

    if user.role==User.nodal_officer:
        
        # print("nodal")

        # print(user.ref_user)

        case=cases.objects.filter(user=userid)


        total=0
        won=0
        defeat=0
        pending=0

        for i in case:
            # print(i)
            total+=1

            
            if i.decision_sought==cases.won:
                won+=1
            elif i.decision_sought==cases.defeat:
                defeat+=1
            elif i.decision_sought==cases.pending:
                pending+=1
        
        # print(total)

        law_objs = user_lawyer.objects.filter(user=user)

        total_lawyer=0

        for i in law_objs:
            # print(i.lawyer)
            total_lawyer+=1

        user = User.objects.filter(ref_user=user)

        total_user=0

        for i in user:
            # print(i)
            total_user+=1

        try:

            won_per = (round((won/total)*100,1))
            def_per = (round((defeat/total)*100,1))
            pen_per = (round((pending/total)*100,1))
        except:
            won_per=0
            def_per=0
            pen_per=0
            
            return render(request,'Dashboard/nodal_officer/Dashboard.html',{'user':userid,'total':total,'won':won,'defeat':defeat,'pending':pending,'lawyers':total_lawyer,'users':total_user,'won_per':won_per,'def_per':def_per,'pen_per':pen_per})

        # print(won_per,def_per,pen_per)

        return render(request,'Dashboard/nodal_officer/Dashboard.html',{'user':userid,'total':total,'won':won,'defeat':defeat,'pending':pending,'lawyers':total_lawyer,'users':total_user,'won_per':won_per,'def_per':def_per,'pen_per':pen_per})

    elif user.role==User.head :
        # print("Hi Head")

        case=cases.objects.filter(user=user.ref_user)

        total=0
        won=0
        defeat=0
        pending=0

        for i in case:
            print(i)
            total+=1

            print(i.decision_sought)
            if i.decision_sought==cases.won:
                won+=1
            elif i.decision_sought==cases.defeat:
                defeat+=1
            elif i.decision_sought==cases.pending:
                pending+=1
        
        print(total)

        law_objs = user_lawyer.objects.filter(user=user.ref_user)

        total_lawyer=0

        for i in law_objs:
            # print(i.lawyer)
            total_lawyer+=1

        won_per = (round((won/total)*100,1))
        def_per = (round((defeat/total)*100,1))
        pen_per = (round((pending/total)*100,1))

        return render(request,'HeadDashboard/Dashboard.html',{'user':userid,'total':total,'won':won,'defeat':defeat,'pending':pending,'lawyers':total_lawyer,'won_per':won_per,'def_per':def_per,'pen_per':pen_per})
    
    elif user.role==User.superadmin:

        
        return render(request,'SuperAdmin/Dashboard.html',{'user':userid})


@login_required(login_url='/login/')
def nodalmanageprofile(request,userid):

    user=User.objects.get(pk=userid)

    if user.role==User.nodal_officer:

        nodal = User.objects.get(pk=userid)

        # print(nodal)

        return render(request,'Dashboard/nodal_officer/Profile.html',{'user':userid,'nodal':nodal})
    elif user.role==User.head:

        head = User.objects.get(pk=userid)

        return render(request,'HeadDashboard/Profile.html',{'user':userid,'head':head})

    elif user.role==User.superadmin:

        user = User.objects.get(pk=userid)

        return render(request,'SuperAdmin/Profile.html',{'user':userid,'admin':user})

@login_required(login_url='/login/')
def neditprofile(request,userid):
    user=User.objects.get(pk=userid)

    if user.role==User.nodal_officer:

        nodal = User.objects.get(pk=userid)

        # print(nodal)

        return render(request,'Dashboard/nodal_officer/EditProfile.html',{'user':userid,'nodal':nodal})
    elif user.role==User.head:
        head = User.objects.get(pk=userid)

        return render(request,'HeadDashboard/EditProfile.html',{'user':userid,'head':head})

@login_required(login_url='/login/')
def updatenodal(request,userid):

    user=User.objects.get(pk=userid)

    if request.method=='POST':

        user=User.objects.get(pk=userid)

        if user.role==User.nodal_officer:

            nodal = User.objects.get(pk=userid)

            nodal.first_name = request.POST.get('first_name')
            nodal.middle_name = request.POST.get('middle_name')
            nodal.last_name=request.POST.get('last_name')
            nodal.email=request.POST.get('email').lower()
            nodal.contact_no=request.POST.get('contact_no')
            
            print(nodal.org,type(nodal.org))

            org = nodal.org

            print(org.pk)
            
            org.name=request.POST.get('org_name').lower()
            org.address=request.POST.get('address').lower()
            org.city=request.POST.get('city').lower()

            print(nodal.dept)

            dept = nodal.dept

            print(dept.pk)

            dept.name=request.POST.get('dept_name').lower()

            # print(first_name,middle_name,last_name,email,contact_no,org_name,dept_name,address,city)
            
            
            dept.save()

            org.save()

            nodal.save()

            

            return render(request,'Dashboard/nodal_officer/Profile.html',{'user':userid,'nodal':nodal})

        elif user.role==User.head:

            head = User.objects.get(pk=userid)

            head.first_name = request.POST.get('first_name')
            head.middle_name = request.POST.get('middle_name')
            head.last_name=request.POST.get('last_name')
            head.email=request.POST.get('email').lower()

            head.save()

            return render(request,'HeadDashboard/Profile.html',{'user':userid,'head':head})            
    if user.role==User.nodal_officer:  

        nodal = User.objects.get(pk=userid)

        return render(request,'Dashboard/nodal_officer/Profile.html',{'user':userid,'nodal':nodal})
    else:
        head = User.objects.get(pk=userid)

        return render(request,'HeadDashboard/Profile.html',{'user':userid})


@login_required(login_url='/login/')
def updatenodalpassword(request,userid):

    user = User.objects.get(pk=userid)

    # print(user.role)

    if request.method=='POST':

        user = User.objects.get(pk=userid)

        # print(user.role)

        if user.role==User.nodal_officer:

            nodal = User.objects.get(pk=userid)

            cur_password = request.POST.get('currentPassword')

            password = request.POST.get('password')

            # print(check_password(cur_password,nodal.password))
            
            if check_password(cur_password,nodal.password):
            
                nodal.set_password(password)

                nodal.save()

                return render(request,'Dashboard/nodal_officer/Profile.html',{'user':userid,'nodal':nodal})
            else:
                
                messages.info(request,'Your Current Password Is Wrong')

                return render(request,'Dashboard/nodal_officer/changePassword.html',{'user':userid})
        elif user.role==User.head:
            
            print("head")

            head = User.objects.get(pk=userid)

            cur_password = request.POST.get('currentPassword')

            password = request.POST.get('password')

            # print(check_password(cur_password,head.password))
            
            if check_password(cur_password,head.password):
            
                head.set_password(password)

                head.save()

                return render(request,'HeadDashboard/Profile.html',{'user':userid,'head':head})
            else:
                
                messages.info(request,'Your Current Password Is Wrong')

                return render(request,'HeadDashboard/changePassword.html',{'user':userid})

        elif user.role==User.superadmin:
            sadmin = User.objects.get(pk=userid)

            cur_password = request.POST.get('currentPassword')

            password = request.POST.get('password')

            # print(check_password(cur_password,head.password))
            
            if check_password(cur_password,sadmin.password):
            
                sadmin.set_password(password)

                sadmin.save()

                return render(request,'SuperAdmin/Profile.html',{'user':userid,'sadmin':sadmin})
            else:
                
                messages.info(request,'Your Current Password Is Wrong')

                return render(request,'SuperAdmin/changePassword.html',{'user':userid})

    else:

        if user.role==User.nodal_officer:  

            return render(request,'Dashboard/nodal_officer/changePassword.html',{'user':userid})
        elif user.role==User.head:

            return render(request,'HeadDashboard/changePassword.html',{'user':userid})
        elif user.role==User.superadmin:
            
            return render(request,'SuperAdmin/changePassword.html',{'user':userid})
        

@login_required(login_url='/login/')  
def addlawyer(request,userid):

    if request.method=="POST":
        
        first_name = request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name=request.POST.get('last_name')
        contact_no=request.POST.get('contact_no')
        email=request.POST.get('email')
        address=request.POST.get('address')

        print(first_name,middle_name,last_name,email,contact_no,address)

        if lawyers.objects.filter(first_name=first_name,middle_name=middle_name,last_name=last_name,email=email,address=address).exists():
            
            law=lawyers.objects.filter(first_name=first_name,middle_name=middle_name,last_name=last_name,email=email,address=address)

            user_l = User.objects.get(pk=userid)                 # get the user object

            print()

            if user_lawyer.objects.filter(lawyer__in=law,user=user_l):
                messages.info(request,'This Lawyer Is Already Exists')

                return render(request,'Dashboard/nodal_officer/Add_Lawyer.html',{'user':userid})                            # for Add_Lawyer.html
            else:
                law=lawyers.objects.filter(first_name=first_name,middle_name=middle_name,last_name=last_name,email=email,address=address)[:1].get()

                nodal = User.objects.get(pk=userid)                 # get the user object

                u_lawyer=user_lawyer.objects.create(user=nodal,lawyer=law)        # create user_lawyer object

                # log_table.objects.create(lawyer=law)

                return redirect('/viewlawyer/'+str(userid))


        lawyer = lawyers.objects.create(first_name=first_name,middle_name=middle_name,last_name=last_name
        ,contact_no=contact_no,email=email,address=address)                 # create the lawyer object


        # log_table.objects.create(lawyer=lawyer)

        nodal = User.objects.get(pk=userid)                 # get the user object

        u_lawyer=user_lawyer.objects.create(user=nodal,lawyer=lawyer)        # create user_lawyer object

        

        return redirect('/viewlawyer/'+str(userid))
    else:

        return render(request,'Dashboard/nodal_officer/Add_Lawyer.html',{'user':userid})                            # for Add_Lawyer.html

@login_required(login_url='/login/')
def viewlawyer(request,userid):

    user=User.objects.get(pk=userid)
    
    if user.role==User.nodal_officer:  

        if request.method=='POST':
            primarykey=request.POST.get('primarykey')

            law  = user_lawyer.objects.filter(user=userid,lawyer=int(primarykey))[:1].get()

            print(law,law.lawyer)

            o_law=law.lawyer

            o_law.first_name = request.POST.get('first_name')
            o_law.middle_name = request.POST.get('middle_name')
            o_law.last_name = request.POST.get('last_name')
            o_law.email=request.POST.get('email').lower()
            o_law.contact_no=request.POST.get('contact_no')
            o_law.address=request.POST.get('address')
            
            o_law.save()
        else:
            u_lawyer =user_lawyer.objects.filter(user=userid)

            lawyers=[]

            for i in u_lawyer:
                lawyers.append(i.lawyer)

            return render(request,'Dashboard/nodal_officer/View_Lawyer.html',{'user':userid,'lawyers':lawyers})
    elif user.role==User.head:

        u_lawyer =user_lawyer.objects.filter(user=user.ref_user.pk)

        lawyers=[]

        for i in u_lawyer:
            lawyers.append(i.lawyer)

        return render(request,'HeadDashboard/View_Lawyer.html',{'user':userid,'lawyers':lawyers})

    elif user.role==User.superadmin:

        lawyer = user_lawyer.objects.all()

        return render(request,'SuperAdmin/View_Lawyer.html',{'user':userid,'lawyers':lawyer})

    if user.role==User.head:

        u_lawyer =user_lawyer.objects.filter(user=user.ref_user.pk)

        lawyers=[]

        for i in u_lawyer:
            lawyers.append(i.lawyer)

        return render(request,'HeadDashboard/View_Lawyer.html',{'user':userid,'lawyers':lawyers})

    else:
        u_lawyer =user_lawyer.objects.filter(user=userid)

        lawyers=[]

        for i in u_lawyer:
            lawyers.append(i.lawyer)

        return render(request,'Dashboard/nodal_officer/View_Lawyer.html',{'user':userid,'lawyers':lawyers})


@login_required(login_url='/login/')
def deletelawyer(request,lawyerid,userid):

    law = user_lawyer.objects.filter(user=userid,lawyer=lawyerid)[:1].get()

    lawyer = law.lawyer

    # log_table.objects.create(lawyer=lawyer)

    # print(law.lawyer,type(law.lawyer))

    case_l = case_lawyers.objects.filter(lawyer=law.lawyer)

    case_l.delete()
    
    law.delete()

    return redirect('/viewlawyer/'+str(userid))

@login_required(login_url='/login/')
def adduser(request,userid):

    if request.method=='POST':

        # print(request)

        first_name=request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name = request.POST.get('last_name')

        email = request.POST.get('email')

        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password == confirmpassword:
            # print(first_name,middle_name,last_name,email,password,confirmpassword)

            num = random.randint(1000,10000)
            name=first_name+str(num)

            while User.objects.filter(username=num).exists():
                num = random.randint(1000,10000) 
                name=first_name+str(num)
            
            # print(name)

            ref = User.objects.get(pk=userid)

            if User.objects.filter(ref_user=ref,first_name=first_name,middle_name=middle_name,last_name=last_name,email=email):

                messages.info(request,'this user is already registered')

                return render(request,'Dashboard/nodal_officer/Add_User.html',{'user':userid})
            else:
                user = User.objects.create_user(username=name,first_name=first_name,middle_name=middle_name,last_name=last_name,ref_user=ref,email=email,password=password,org=ref.org,dept=ref.dept,role=User.head)   

                log_table.objects.create(user=user)

                # print(user.username,user.role)

                return redirect('/viewuser/'+str(userid))

        else:

            messages.info(request,'Your Password Does\'nt matched')

            return render(request,'Dashboard/nodal_officer/Add_User.html',{'user':userid})

    return render(request,'Dashboard/nodal_officer/Add_User.html',{'user':userid})

@login_required(login_url='/login/')
def viewuser(request,userid):

  
    ref = User.objects.get(pk=userid)

    users = User.objects.filter(ref_user=ref)

    # print(users)

    return render(request,'Dashboard/nodal_officer/View_User.html',{'user':userid,'other_users':users})

@login_required(login_url='/login/')
def edituser(request,refid,userid):

    if request.method=="POST":
        ref_user = User.objects.get(pk=refid)

        user = User.objects.get(pk=userid)

        print("Reference is : ",ref_user,"User is :",user)

        user.first_name=request.POST.get('first_name')
        user.middle_name=request.POST.get('middle_name')
        user.last_name=request.POST.get('last_name')
        user.email = request.POST.get('email')

        password = request.POST.get('newpassword')

        user.set_password(password)

        user.save()

    return redirect('/viewuser/'+str(refid))

def deleteuser(request,refid,userid):

    user = User.objects.get(pk=userid)

    # print(user)

    user.delete()

    return redirect('/viewuser/'+str(refid))

def search(request,userid):

    user = User.objects.get(pk=userid)

    case=None

    if request.method=="POST":

        search_txt=request.POST.get('search')
        if search_txt != "":
            case = cases.objects.filter(case_synopsis__icontains=search_txt)

            for i in case:

                print(i.case_synopsis)

    if user.role==User.nodal_officer:
        
        return render(request,'Dashboard/nodal_officer/Search.html',{'user':userid,'case':case})
    elif user.role==User.head:

        return render(request,'HeadDashboard/Search.html',{'user':userid,'case':case})
    elif user.role==User.superadmin:
        return render(request,'SuperAdmin/Search.html',{'user':userid,'case':case})


def viewsearch(request,caseid):

    case = cases.objects.get(pk=caseid)


    if case_lawyers.objects.filter(case=caseid).exists():
        case_l = case_lawyers.objects.filter(case=caseid)[:1].get()
    else:
        case_l = None

    hearings=case_hearings.objects.filter(case=case)

    return render(request,'SuperAdmin/View_Search_Details.html',{'case':case,'case_lawyer':case_l,'hearings':hearings})
