from django.shortcuts import render
from home.models import Hotel ,Ameneties,HotelUser,HotelBooking
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime 


# Create your views here.


def index(request):
    hotels=Hotel.objects.all()
    ameneties=Ameneties.objects.all()
    if request.GET.get('serach'):
        hotels=hotels.filter(hotel_name__icontains=request.GET.get('serach'))
    
    if request.GET.get('sort_by'):
        sort_by=request.GET.get('sort_by')
        if sort_by=="sort_low":
            hotels=hotels.order_by("hotel_offer_price")
        elif sort_by == "sort_high":
            hotels=hotels.order_by('-hotel_offer_price') 
    return render(request,'index.html',context={'hotels': hotels,'ameneties':ameneties})

def hotel_details(request,slug):
    hotels=Hotel.objects.all()
    hotel=Hotel.objects.get(hotel_slug=slug)
    
    if request.method =="POST":
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        
        start_date=datetime.strptime(start_date,'%Y-%m-%d')
        end_date=datetime.strptime(end_date,'%Y-%m-%d')
        
        days_count=(end_date-start_date).days
        
        if days_count <=0:
            messages.warning(request,"Please enter the correct dates ")
            return HttpResponseRedirect(request.path_info)
        
        Booking_details=HotelBooking.objects.create(
            
            hotel=hotel,
            booking_user=HotelUser.objects.get(id = request.user.id),
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=hotel.hotel_offer_price * days_count,
  
        )
        
        messages.success(request,"Booking Captured")
        return HttpResponseRedirect(request.path_info)
    
    return render(request,'hotel_details.html',context={'hotel':hotel,'Booking_details':Booking_details})
