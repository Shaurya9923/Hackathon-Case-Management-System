from django.urls import path
from . import views

urlpatterns = [
    path('nodaldashboard/<int:userid>/',views.nodaldashboard,name='nodaldashboard'),      # for nodal_officer => Dashboard.html
    path('nodalmanageprofile/<int:userid>/',views.nodalmanageprofile,name='nodalmanageprofile'),         # for nodal_officer => Profile.html
    path('neditprofile/<int:userid>/',views.neditprofile,name='neditprofile'),                  # for nodal_officer =>EditProfile.html
    path('updatenodal/<int:userid>/',views.updatenodal,name='updatenodal'),                        # for update the user
    path('updatenodalpassword/<int:userid>/',views.updatenodalpassword,name='updatenodalpassword'),      # for changepassword.html
    path('addlawyer/<int:userid>/',views.addlawyer,name='addlawyer'),        # for Add_Lawyer.html
    path('viewlawyer/<int:userid>/',views.viewlawyer,name='viewlawyer'),      # for View_Lawyer.html
    path('deletelawyer/<int:lawyerid>/<int:userid>/',views.deletelawyer,name='deletelawyer'),       # for delete the lawyer
    path('adduser/<int:userid>',views.adduser,name="adduser"),               # for Add_User.html
    path('viewuser/<int:userid>',views.viewuser,name="viewuser"),            # for View_User.html
    path('edituser/<int:refid>/<int:userid>',views.edituser,name="edituser"),       # for edit the user
    path('deleteuser/<int:refid>/<int:userid>',views.deleteuser,name="deleteuser"),     # for deleteuser 
    path('search/<int:userid>',views.search,name='search'),                              # for Search.html
    path('viewsearch/<int:caseid>',views.viewsearch,name='viewsearch'),                     # for View_Search_Details.html
    
]

