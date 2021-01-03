from django.urls import path
from . import views

urlpatterns = [

    path('notification/',views.notification,name='notification'),
    path('addcase/<int:userid>/',views.addcase,name='addcase'),             # for Add_Case.html
    path('viewcase/<int:userid>/',views.viewcase,name='viewcase'),          # for View_case.html
    path('viewcasedetails/<int:userid>/<int:caseid>',views.viewcasedetails,name='viewcasedetails'),     # for View_Case_Details.html
    path('editcase/<int:userid>/<int:caseid>',views.editcase,name='editcase'),                          # for EditCase.html
    path('edithearing/<int:userid>/<int:caseid>',views.edithearing,name='edithearing'),     # for edit the hearing
    path('addhearing/<int:userid>/<int:caseid>',views.addhearing,name='addhearing'),        # for add hearing 
    path('invoicenodal/<int:userid>/',views.invoicenodal,name='invoicenodal'),                             # for Invoice.html
    path('viewinvoice/<int:userid>/<int:caseid>',views.viewinvoice,name='viewinvoice'),                  # for View_Invoice.html
    path('editinvoice/<int:userid>/<int:caseid>/',views.editinvoice,name='editinvoice'),         # for edit the invoice
    path('deletecase/<int:userid>/<int:caseid>',views.deletecase,name='deletecase'),                          # for deletecase
    path('notify/<int:userid>/',views.notify,name='notify'),                                    # for Notification.html
]