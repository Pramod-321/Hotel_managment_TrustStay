from django.contrib import admin
from home.models import HotelUser,HotelVendor,Ameneties,Hotel
# Register your models here.

admin.site.register(HotelUser)
admin.site.register(HotelVendor)
admin.site.register(Ameneties)
admin.site.register(Hotel)