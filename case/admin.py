from django.contrib import admin
from .models import cases,case_lawyers,case_hearings,case_invoices,lawyers,user_lawyer,log_table 
# Register your models here.

admin.site.register(cases)
admin.site.register(lawyers)
admin.site.register(case_lawyers)
admin.site.register(case_hearings)
admin.site.register(case_invoices)
admin.site.register(user_lawyer)
admin.site.register(log_table)