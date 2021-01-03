from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),         # for signup.html
    path('login/',views.login,name="login"),            # for login.html
    path('logout/',views.logout,name="logout"),         # for logout
    path('requestlog/<int:userid>/',views.requestlog,name="requestlog"),      # for superadmin RequestLog
    path('do_accept/<int:userid>/<int:refid>',views.do_accept,name='do_accept'),          # for accepting
    path('do_reject/<int:userid>/<int:refid>',views.do_reject,name='do_reject'),          # for accepting
    
]

