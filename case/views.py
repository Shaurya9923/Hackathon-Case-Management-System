from django.shortcuts import render,redirect
from .models import cases,lawyers,user_lawyer,case_lawyers,case_hearings,case_invoices,log_table
from court.models import Court,Court_Type,Practice_Area
from core.models import User
from django.http import HttpResponse
from django.contrib import messages
from .forms import case_form,hearing_form,invoice_form
# from types import NoneType

from django.contrib.auth.decorators import login_required

from datetime import datetime  
from datetime import timedelta
# for email 
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core import mail
import time
# Create your views here.

def notification(request):
    
    case = cases.objects.all()
    cases_obj=[]
    
    for i in case:

        caseId=i.case_number
        caseTitle=i.title
        caseSyno=i.case_synopsis
        title=i.title
        court=i.court

        # print(i.next_hearing_at,type(i.next_hearing_at))
        hdate = i.next_hearing_at
        todi = datetime.now().date()
        diff = (hdate-todi)

        

        tme ='12:35'

        

        if diff == timedelta(days=10):
            # cases_obj.append(i)
            
            # ahiyan haji Headof the department ne mail pochadva no baki che 

            html_content = render_to_string("notification/email_template.html",{'id':caseId,'caseTitle':caseTitle+str(i.pk),'caseSyno':caseSyno,'title':title,'court':court})
            text_content = strip_tags(html_content)

            if tme==time.strftime('%H:%M'):
                email = EmailMultiAlternatives(
                    #subject
                    "testing",
                    #content
                    text_content,
                    #from email
                    settings.EMAIL_HOST_USER,
                    # rec list
                    [i.user.email]
                )

                
                email.attach_alternative(html_content,"text/html")
                email.send()

        str1="Only One Day is Left"
    
    return HttpResponse("Email Has Been Sent")


@login_required(login_url='/login/')
def addcase(request,userid):

    if request.method=='POST':

        type = request.POST.get('type').lower() # take a type and match with current type

        case_number = request.POST.get('case_number')
    
        if Practice_Area.objects.filter(name__startswith=type).exists():
            print(type)

            pr_area = Practice_Area.objects.filter(name__startswith=type)[:1].get()
        else:
            pr_area = Practice_Area.objects.create(name=type)

            print(pr_area.name,pr_area.pk)

        lawyer_name = request.POST['lawyer']    # take a lawyer id and check from existing

        l_n = lawyer_name.split()

        # print("Hi ",l_n)

        if len(l_n)>=3:
        
            if lawyers.objects.filter(first_name=l_n[0],middle_name=l_n[1],last_name=l_n[2]).exists():

                lawyer_obj = lawyers.objects.get(first_name=l_n[0],middle_name=l_n[1],last_name=l_n[2])
            else:
                lawyer_obj=None
        else:

            messages.info(request,"please Give The Full Name")

            form = case_form()

            crts=Court.objects.all()

            return render(request,'Dashboard/nodal_officer/Add_Case.html',{'user':userid,'courts':crts,'form':form})              # for Add_Case.html


        user_l = User.objects.get(pk=userid)

        # print(user_lawyer.objects.filter(lawyer__in=lawyer,user=user_l))

        if user_lawyer.objects.filter(lawyer=lawyer_obj,user=user_l).exists():
            
            u_lawyer = user_lawyer.objects.filter(lawyer=lawyer_obj,user=user_l)[:1].get()

            print(u_lawyer.lawyer.first_name)
        else:
            messages.info(request,"please select lawyer from your existing list or add a new lawyer")

            form = case_form()

            crts=Court.objects.all()

            return render(request,'Dashboard/nodal_officer/Add_Case.html',{'user':userid,'courts':crts,'form':form})              # for Add_Case.html

        court = request.POST.get('court')

        c_n=(court.split('of'))

        court_type =c_n[0]                 # for court_type

        if Court_Type.objects.filter(name__startswith=court_type).exists():
           c_type = Court_Type.objects.filter(name__startswith=court_type)[:1].get() 

           print(c_type.name)
        else:
            c_type = Court_Type.objects.create(name=court_type)

            print(c_type.name,c_type.pk)

        
        court_place = c_n[1]

        print(Court.objects.filter(place__startswith=court_place,court_type=c_type))

        if Court.objects.filter(place__startswith=court_place,court_type=c_type).exists():

            court = Court.objects.filter(place__startswith=court_place,court_type=c_type)[:1].get()

            print(court.court_type,court.place)
        else:
            court = Court.objects.create(place=court_place,court_type=c_type)

            print(court.court_type,court.place,court.pk)

        title = request.POST.get('casesubject').lower()

        # oponent details

        opo_name = request.POST.get('opo_name').lower()
        opo_contact_no = request.POST.get('opo_contact_no').lower()
        opo_email = request.POST.get('opo_email').lower()
        opo_address = request.POST.get('opo_address').lower()

        # case details 

        case_desc = request.POST.get('case_desc')

        form = case_form(request.POST,request.FILES)

        if form.is_valid():

            detail_doc = form.cleaned_data.get('detail_doc')
            reply = form.cleaned_data.get('reply')
            rejoinder =form.cleaned_data.get('rejoinder') 

        print(detail_doc)

        nxt_hearing = request.POST.get('nxt_hearing')

        

        # print(request)

        caseresult = request.POST.get('caseresult')


        print(caseresult)

        if caseresult==cases.pending:
            result = cases.pending
        elif caseresult == cases.won:
            result = cases.won
        elif caseresult==cases.defeat:
            result = cases.defeat

        casestatus = request.POST.get('casestatus')
        case_priority = request.POST.get('case_priority')
        print(casestatus)
        case_reminder = request.POST.get('case_reminder')

        action_taken = request.POST.get('action_taken')

        case_obj = cases.objects.create(user=user_l,court = court,case_number=case_number,case_priority=case_priority,case_reminder=case_reminder,status=casestatus,type = pr_area,title = title
        ,case_synopsis= case_desc,detail_doc = detail_doc,reply=reply,rejoinder=rejoinder,action_taken=action_taken
        ,opponent_name = opo_name,opponent_contact_no = opo_contact_no
        ,opponent_email = opo_email,opponent_address = opo_address,next_hearing_at = nxt_hearing
        ,decision_sought = result)
        
        lawyer_obj = lawyers.objects.get(first_name=l_n[0],middle_name=l_n[1],last_name=l_n[2])

        case_lawyer_obj = case_lawyers.objects.create(case=case_obj,lawyer=lawyer_obj)

        case_hearing_obj=case_hearings.objects.create(hearing_at=nxt_hearing,case=case_obj,user=user_l,order_type=case_hearings.Interim)

        case_invoices.objects.create(case=case_obj,hearing=case_hearing_obj,payment_status=case_invoices.unpaid)

        return redirect('/viewcase/'+str(userid))

    form = case_form()

    # print(request)

    u_lawyer =user_lawyer.objects.filter(user=userid)

    laws=[]

    for i in u_lawyer:
        name=i.lawyer.first_name+" "+i.lawyer.middle_name+" "+i.lawyer.last_name
        laws.append(name)

    print(laws)

    crts=Court.objects.all()

    for i in crts:
        print(i)

    return render(request,'Dashboard/nodal_officer/Add_Case.html',{'user':userid,'form':form,'courts':crts,'lawyers':laws})              # for Add_Case.html

@login_required(login_url='/login/')
def viewcase(request,userid):

    user = User.objects.get(pk=userid)

    print(user.role)

    # print(user.ref_user)

    if user.role==User.nodal_officer:

        all_cases = cases.objects.filter(user=userid)

        case_l=[]

        for i in all_cases:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))

        # print(case_l)

        # for i in case_l:
        #     print(i)
        #     for j in i:
        #         print(j)

        return render(request,'Dashboard/nodal_officer/View_Case.html',{'user':userid,'cases':all_cases,'case_lawyer':case_l})                            # for Views_Case.html

    elif user.role==User.head:

        # print(user.ref_user)

        all_cases = cases.objects.filter(user=user.ref_user)

        case_l=[]

        for i in all_cases:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))



        return render(request,'HeadDashboard/View_Case.html',{'user':userid,'cases':all_cases,'case_lawyer':case_l})
    elif user.role==User.superadmin:

        case = cases.objects.all()

        case_l=[]

        for i in case:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))

        return render(request,'SuperAdmin/View_Case.html',{'user':user.pk,'cases':case,'case_lawyer':case_l})

@login_required(login_url='/login/')
def viewcasedetails(request,userid,caseid):

    user = User.objects.get(pk=userid)

    print(user.role)

    # print(caseid)
    if user.role==User.nodal_officer:

        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():
            case_l = case_lawyers.objects.filter(case=caseid)[:1].get()
        else:
            case_l = None

        user = User.objects.get(pk=userid)

        hearings=case_hearings.objects.filter(case=case,user=user)

        nxt_hear =case.next_hearing_at.strftime("%b %d,%Y")

        hear_date=datetime.strptime(nxt_hear, '%b %d,%Y').strftime('%Y-%m-%d')

        # print(hear_date)

        form = hearing_form()

        return render(request,'Dashboard/nodal_officer/View_Case_Details.html',{'user':userid,'case':case,'case_lawyer':case_l,'h_date':hear_date,'hearings':hearings,'form':form})             # for View_Case_Details.html
    
    elif user.role==User.head:

        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():
            case_l = case_lawyers.objects.filter(case=caseid)[:1].get()
        else:
            case_l = None

        hearings=case_hearings.objects.filter(case=case,user=user.ref_user)

        return render(request,'HeadDashboard/View_case_Details.html',{'user':userid,'case':case,'case_lawyer':case_l,'hearings':hearings})

    elif user.role==User.superadmin:

        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():
            case_l = case_lawyers.objects.filter(case=caseid)[:1].get()
        else:
            case_l = None

        hearings=case_hearings.objects.filter(case=case)

        return render(request,'SuperAdmin/View_case_Details.html',{'user':userid,'case':case,'case_lawyer':case_l,'hearings':hearings})


        return render(request,'SuperAdmin/View_case_Details.html',{'user':user.pk,'case':1})

@login_required(login_url='/login/')
def editcase(request,userid,caseid):
    
    case = cases.objects.get(pk=caseid)

    if request.method=='POST':
        # print(request)

        case.title = request.POST.get('title')

        case.opponent_name=request.POST.get('opponent_name')
        case.opponent_email =request.POST.get('opponent_email')
        case.opponent_contact_no = request.POST.get('opponent_contact_no')
        case.opponent_address = request.POST.get('opponent_address')
        case.decision_sought = request.POST.get('result')
        case.case_synopsis = request.POST.get('case_synopsis')

        case.case_priority=int(request.POST.get('case_priority'))

        lawyer_name = request.POST.get('lawyer')

        l_n = lawyer_name.split()

        print(l_n)

        if len(l_n)>=3:
            if lawyers.objects.filter(first_name=l_n[0],middle_name=l_n[1],last_name=l_n[2]).exists():

                lawyer = lawyers.objects.get(first_name=l_n[0],middle_name=l_n[1],last_name=l_n[2])

                user = User.objects.get(pk=userid)

                if user_lawyer.objects.filter(user=user,lawyer=lawyer).exists():
                    u_lawyer = user_lawyer.objects.get(user=user,lawyer=lawyer)
                    
                    if case_lawyers.objects.filter(case=case,lawyer=u_lawyer.lawyer).exists():

                        print(case_lawyers.objects.filter(case=case,lawyer=u_lawyer.lawyer))
                        p_lawyer = case_lawyers.objects.get(case=case,lawyer=u_lawyer.lawyer)

                    else:
                    
                        if case_lawyers.objects.filter(case=case).exists():

                            case_juno_lawyer=case_lawyers.objects.get(case=case)

                            print(case_juno_lawyer.lawyer)

                            case_juno_lawyer.delete()

                        n_lawyer = case_lawyers.objects.create(case=case,lawyer=lawyer)


                else:
            
                    messages.info(request,"Please Select the lawyer from lawyers list ")

                    result=['won','defeat','pending']

                    form = case_form()

                    return render(request,'Dashboard/nodal_officer/EditCase.html',{'user':userid,'case':case,'result':result,'form':form})
            else:
            
                messages.info(request,"Please Select the lawyer from lawyers list ")


                result=['won','defeat','pending']

                form = case_form()

                return render(request,'Dashboard/nodal_officer/EditCase.html',{'user':userid,'case':case,'result':result,'form':form})
        else:

            messages.info(request,"Please Give full Name ")

            result=['won','defeat','pending']

            form = case_form()

            return render(request,'Dashboard/nodal_officer/EditCase.html',{'user':userid,'case':case,'result':result,'form':form})

        rp_doc = cases.reply

        rj_doc = cases.rejoinder

        # case.reply = rp_doc
        # case.rejoinder = rj_doc

        form =case_form(request.POST,request.FILES)


        if form.is_valid():

            reply = form.cleaned_data.get('reply')

            rejoinder = form.cleaned_data.get('rejoinder')

            # print(type(detail_doc))

            if type(reply) == type(None):
                pass
            else:
                case.reply = reply

            if type(rejoinder) == type(None):
                pass
            else:
                case.rejoinder= rejoinder
              
        case.save()

        return redirect('/viewcasedetails/'+str(userid)+"/"+str(caseid))

    if  case_lawyers.objects.filter(case=caseid).exists():
        case_l = case_lawyers.objects.filter(case=caseid)[:1].get()
    else:
        case_l=None

    form=case_form()

    result=['won','defeat','pending']

    return render(request,'Dashboard/nodal_officer/EditCase.html',{'user':userid,'case':case,'case_lawyer':case_l,'result':result,'form':form})             # for View_Case_Details.html    


@login_required(login_url='/login/')
def addhearing(request,userid,caseid):

    case = cases.objects.get(pk=caseid)

    user = User.objects.get(pk=userid)

    

    if request.method=='POST':

        # print("prev is ",case.next_hearing_at)

        prev_hearing=case.next_hearing_at

        cash_hr_pr = case_hearings.objects.get(case=case,user=user,hearing_at=prev_hearing)     # previous

        # print(cash_hr_pr)

        next_hearing = request.POST.get('next_hearing')

        # print("next is",next_hearing_at,)

        # print(cash_hr_pr.hearing_at-next_hearing_at)

        # print(next_hearing)

        next_hearing_at = datetime.strptime(next_hearing,'%Y-%m-%d').date()

        # print(next_hearing_at-cash_hr_pr.hearing_at,type(next_hearing_at-cash_hr_pr.hearing_at))
        
        diff=next_hearing_at-cash_hr_pr.hearing_at

        # print(diff.days,type(diff.days))

        if diff.days>0:
            # print("Not Zero",diff.days,type(diff.days))
            case.next_hearing_at=next_hearing_at                # set next hearing

            case_hearing_obj=case_hearings.objects.create(hearing_at=next_hearing_at,case=case,user=user,prev_hearing=cash_hr_pr)

            case.save()

            case_l = case_lawyers.objects.get(case=caseid)

            lawyer_obj=case_l.lawyer

            case_invoices.objects.create(case=case,hearing=case_hearing_obj,payment_status=case_invoices.unpaid)
        else:
            messages.info(request,"This date is not valid for Next Hearing")

    return redirect('/viewcasedetails/'+str(userid)+"/"+str(caseid))


@login_required(login_url='/login/')
def edithearing(request,userid,caseid):

    if request.method=="POST":
        
        print(request)

        case = cases.objects.get(pk=caseid)

        user = User.objects.get(pk=userid)

        hearing_at = request.POST.get('hearing_at')

        # print(hearing_at)
        
        
        try:
            h_date =datetime.strptime(hearing_at,'%b. %d, %Y').date()

            # print("with date",h_date)
        except:
            try:
                h_date =datetime.strptime(hearing_at,'%B %d, %Y').date()

                # print("without date ",h_date)
            except:
                try:
                    h_date =datetime.strptime(hearing_at,'%b %d, %Y').date()
                except:
                    h_date =datetime.strptime(hearing_at,'%B. %d, %Y').date()


        # print(h_date)

        c_h = case_hearings.objects.get(case=case,user=user,hearing_at=h_date)

        print(c_h)

        desc = c_h.description

        o_type=request.POST.get('order_type')

        if o_type==case_hearings.Final:

            c_h.order_type=case_hearings.Final
        elif o_type==case_hearings.Interim:
            c_h.order_type=case_hearings.Interim

        description= request.POST.get('description')

        if description=="":
            c_h.description=desc
        else:
            c_h.description = description

        doc=c_h.detail_doc

        c_h.detail_doc=doc

        casestatus = request.POST.get('casestatus')

        case.status = casestatus

        c_h.status = casestatus        

        form = hearing_form(request.POST,request.FILES)

        if form.is_valid():

            detail_doc = form.cleaned_data.get('detail_doc')

            print(type(detail_doc))

            if type(detail_doc) == type(None):
                pass
            else:
                c_h.detail_doc = detail_doc


        # print(hearing_at,prev_hearing,description,casestatus)

        c_h.save()

        case.save()

    return redirect('/viewcasedetails/'+str(userid)+"/"+str(caseid))


@login_required(login_url='/login/')
def invoicenodal(request,userid):

    user= User.objects.get(pk=userid)

    if user.role==User.nodal_officer:

        all_cases = cases.objects.filter(user=userid)

        case_l=[]

        for i in all_cases:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))

        return render(request,'Dashboard/nodal_officer/Invoice.html',{'user':userid,'cases':all_cases,'case_lawyer':case_l})
    
    elif user.role==User.head:


        all_cases = cases.objects.filter(user=user.ref_user)

        case_l=[]

        for i in all_cases:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))

        return render(request,'HeadDashboard/Invoice.html',{'user':userid,'cases':all_cases,'case_lawyer':case_l})
    
    elif user.role==User.superadmin:

        case = cases.objects.all()

        case_l=[]

        for i in case:
            
            case_l.append(case_lawyers.objects.filter(case=i.pk))

        return render(request,'SuperAdmin/Invoice.html',{'user':userid,'cases':case,'case_lawyer':case_l})

@login_required(login_url='/login/')
def viewinvoice(request,userid,caseid):

    user = User.objects.get(pk=userid)

    # print(user.role)
    if user.role==User.nodal_officer:
        
        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():

            case_l = case_lawyers.objects.get(case=caseid)

            c_inv = case_invoices.objects.filter(case=case)
        else:
            case_l=None

            c_inv=None

        # lawyer = lawyers.objects.get(lawyer=case_l.lawyer)

        # print(case_l.lawyer.pk)

        form = invoice_form()

        # print(c_inv)

        return render(request,'Dashboard/nodal_officer/View_Invoice.html',{'user':userid,'case':case,'c_l':case_l,'invoices':c_inv,'form':form})

    elif user.role==User.head:

        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():

            case_l = case_lawyers.objects.get(case=caseid)

            c_inv = case_invoices.objects.filter(case=case)
        else:
            case_l=None

            c_inv=None


        return render(request,'HeadDashboard/View_Invoice.html',{'user':userid,'case':case,'c_l':case_l,'invoices':c_inv})
    
    elif user.role==User.superadmin:

        case = cases.objects.get(pk=caseid)

        if case_lawyers.objects.filter(case=caseid).exists():

            case_l = case_lawyers.objects.get(case=caseid)

            c_inv = case_invoices.objects.filter(case=case)
        else:
            case_l=None

            c_inv=None

        return render(request,'SuperAdmin/View_Invoice.html',{'user':userid,'case':case,'c_l':case_l,'invoices':c_inv})

        
@login_required(login_url='/login/')
def editinvoice(request,userid,caseid):

    case = cases.objects.get(pk=caseid)

    if request.method=='POST':
        # print(request)

        hearing_date = request.POST.get('hearing_date')

        # print(hearing_date)

        try:
            h_date =datetime.strptime(hearing_date,'%b. %d, %Y').date()

            # print("with date",h_date)
        except:
            try:
                h_date =datetime.strptime(hearing_date,'%B %d, %Y').date()

                # print("without date ",h_date)
            except:
                h_date =datetime.strptime(hearing_date,'%b %d, %Y').date()



        cs_h= case_hearings.objects.get(case=case,hearing_at = h_date)

        # print(cs_h)



        c_iv = case_invoices.objects.get(case=case,hearing=cs_h)

        invoice = c_iv.invoice_doc

        c_iv.invoice_doc = invoice

        c_iv.payment_status= request.POST.get('paymentstatus')

        # print(payment_status)

        c_iv.taxable_total = request.POST.get('taxable_total')
        c_iv.gst = request.POST.get('gst')

        form = invoice_form(request.POST,request.FILES)

        if form.is_valid():

            invoice_doc = form.cleaned_data.get('invoice_doc')

            # print(type(invoice_doc))

            if type(invoice_doc) == type(None):
                pass
            else:
                c_iv.invoice_doc = invoice_doc

        c_iv.save()

    return redirect('/viewinvoice/'+str(userid)+"/"+str(caseid))


@login_required(login_url='/login/')
def deletecase(request,userid,caseid):


    case = cases.objects.get(pk=caseid)

    case.delete()

    return redirect('/viewcase/'+str(userid))


@login_required(login_url='/login/')
def notify(request,userid):

    case = cases.objects.all()
    cases_obj=[]
    
    for i in case:

        caseId=i.case_number
        caseTitle=i.title
        caseSyno=i.case_synopsis
        title=i.title
        court=i.court

        # print(i.next_hearing_at,type(i.next_hearing_at))
        hdate = i.next_hearing_at
        todi = datetime.now().date()
        diff = (hdate-todi)

        

        tme ='16:09'

        

        if diff == timedelta(days=10):
            # cases_obj.append(i)
            
            # ahiyan haji Headof the department ne mail pochadva no baki che 

            html_content = render_to_string("notification/email_template.html",{'id':caseId,'caseTitle':caseTitle+str(i.pk),'caseSyno':caseSyno,'title':title,'court':court})
            text_content = strip_tags(html_content)

            if tme==time.strftime('%H:%M'):
                email = EmailMultiAlternatives(
                    #subject
                    "Hearing Notification",
                    #content
                    text_content,
                    #from email
                    settings.EMAIL_HOST_USER,
                    # rec list
                    [i.user.email]
                )

                
                email.attach_alternative(html_content,"text/html")
                email.send()


    user=User.objects.get(pk=userid)

    if user.role==User.nodal_officer:
        case_obj = cases.objects.filter(user=user)

        # print("Hi",case_obj)

        next_cases=[]

        for i in case_obj:
            # print(i.next_hearing_at)

            todi = datetime.now().date()
            diff = (i.next_hearing_at-todi)

            if diff == timedelta(days=10):
                # print(i)
                next_cases.append(i)

        return render(request,'Dashboard/nodal_officer/Notification.html',{'user':userid,'cases':next_cases,'user_obj':user})
    
    elif user.role==User.head:

        case_obj = cases.objects.filter(user=user.ref_user)

        # print("Hi",case_obj)

        next_cases=[]

        for i in case_obj:
            # print(i.next_hearing_at)

            todi = datetime.now().date()
            diff = (i.next_hearing_at-todi)

            if diff == timedelta(days=10):
                # print(i)
                next_cases.append(i)

        return render(request,'HeadDashboard/Notification.html',{'user':userid,'cases':next_cases,'user_obj':user})
    
    elif user.role==User.superadmin:                # for log entry for admin

        logs = log_table.objects.all()

        u_lawyer = user_lawyer.objects.all()

        t_lawyer = lawyers.objects.all()

        return render(request,'SuperAdmin/Notification.html',{'user':userid,'logs':logs,'u_l':u_lawyer,'t_l':t_lawyer})
    

