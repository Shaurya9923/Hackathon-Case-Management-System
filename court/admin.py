from django.contrib import admin
from .models import Court,Court_Type,Practice_Area
# Register your models here.

admin.site.register(Court)
admin.site.register(Court_Type)
admin.site.register(Practice_Area)
