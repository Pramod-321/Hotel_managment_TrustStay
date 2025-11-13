from django.shortcuts import render,redirect
from django.db.models import Q 
from home.models import HotelUser,HotelVendor,Hotel,Ameneties,HotelImages
from .utils import generateRandomToken,sendEmailToken,sendOTPtoEmail,generateSlug
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout,login  as auth_login 
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
def login_page(request):
    if request.method =="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        hotel_user=HotelUser.objects.filter(
            email=email
        )
        
        if not hotel_user.exists():
            messages.warning(request,"User Not Found , kindly Register")
            return redirect('/accounts/login/')
        
        
        if not hotel_user[0].is_verified:
            messages.warning(request,"You are not verified ")
            return redirect('/accounts/login/')
        
        hotel_user=authenticate(username=hotel_user[0].username,password=password)
        
        if hotel_user:
            messages.success(request,"Successfully loged")
            auth_login(request,hotel_user)
            return redirect('/accounts/login/')
        
        messages.warning(request,"invalid credentials ")
        return redirect('/accounts/login/')
        
    return render(request,'login.html')

def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register/')

        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email , hotel_user.email_token)

        messages.success(request, "An email Sent to your Email")
        return redirect('/accounts/register/')


    return render(request, 'register.html')

def verify_email_token(request,token):
    try:
        hotel_user=HotelUser.objects.get(email_token=token)
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request, "Your Email is verified , kindly login")
        return redirect('/accounts/login/')
        
    except Exception as e : 
        return HttpResponse("invalid token")
    
    
    
    
    
def send_otp(request, email):
    print("Received email in send_otp:", email)
    hotel_user = HotelUser.objects.filter(
            email = email)
    if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')

    otp =  random.randint(1000 , 9999)
    hotel_user.update(otp =otp)

    sendOTPtoEmail(email , otp)

    return redirect(f'/accounts/verify-otp/{email}/')


def verify_otp(request,email):
    if request.method=="POST":
        otp=request.POST.get('otp')
        hotel_user=HotelUser.objects.get(email=email)
        
        if otp==hotel_user.otp:
            messages.success(request,"Login success")
            return redirect('/accounts/login/')
        else:
            messages.warning(request,"wrong OTP")
            return redirect(f'/accounts/verify-otp/{email}/')
    
    return render(request,'verify_otp.html',{'email':email})

def register_vendor(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelVendor.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register_vendor/')

        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            business_name=business_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email , hotel_user.email_token)

        messages.success(request, "An email Sent to your Email")
        return redirect('/accounts/register_vendor/')
    
    return render(request,'vendor/register_vendor.html')
  
  
def login_vendor(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(email=email)
        
        if not hotel_user.exists():
            messages.warning(request, "User Not Found, kindly Register")
            return redirect('/accounts/login_vendor/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/account/login-vendor/')
        
        
        hotel_user = authenticate(username = hotel_user[0].username , password=password)
        
     
        print('Hotel_user queryset:', hotel_user)

        
        if hotel_user:
            messages.success(request, "Successfully logged")
            auth_login(request, hotel_user)  # Corrected line here
            return redirect('/accounts/vendor_dashboard/')

        messages.warning(request, "Invalid credentials")
        return redirect('/accounts/login_vendor/')

    return render(request, 'vendor/login_vendor.html')



@login_required(login_url='login_vendor')
def vendor_dashboard(request):
    # Retrieve hotels owned by the current vendor
    hotels = Hotel.objects.filter(hotel_owner=request.user)
    context = {'hotels': hotels}
    return render(request, 'vendor/vendor_dashboard.html', context)



@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method=="POST":
        hotel_name=request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)
        
        hotel_vendor = HotelVendor.objects.get(id = request.user.id)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor
        )
        print(hotel_vendor)

        for amentie in ameneties:
            amentie=Ameneties.objects.get(id=amentie)
            hotel_obj.ameneties.add(amentie)
            hotel_obj.save()
            
        """Inside the loop, this line interacts with the Django database model named Ameneties.
        The Ameneties.objects.get(id=amentie) part is a Django QuerySet method that retrieves a single object 
        from the Ameneties table in the database where the id of the amenity matches the current amentie value from the loop.
        The found amenity object then overwrites the amentie variable.youtube"""
        """This line manages a "many-to-many" relationship between a hotel_obj (a specific hotel) and its amenities. 
        In a Django model, when you have a ManyToManyField, you can use the .add() method to create a link between the two objects. 
        Here, it's adding the amentie object (retrieved in the previous step) to the set of amenities associated with"""


        messages.success(request, "Hotel Created")
        return redirect('/accounts/add_hotel/')


    ameneties=Ameneties.objects.all()
    
    return render(request, 'vendor/add_hotel.html' ,context={'ameneties':ameneties})

    
    
@login_required(login_url='login_vendor')
def upload_image(request,slug):
    hotel_obj=Hotel.objects.get(hotel_slug=slug)
    if request.method =="POST":
        image=request.FILES['image']
        print(image)
        
        HotelImages.objects.create(
            hotel=hotel_obj,
            image=image,
            
        )
        return HttpResponseRedirect(request.path_info)
    return render(request,'vendor/upload_image.html' ,context= {'images' : hotel_obj.hotel_images.all()})


@login_required(login_url='login_vendor')
def delete_image(request,id):
    image_id=HotelImages.objects.get(id=id)
    image_id.delete()
    return redirect('/accounts/vendor_dashboard/')



@login_required(login_url='login_vendor')
def edit_hotel(request,slug):
    hotel_obj=Hotel.objects.get(hotel_slug=slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponseRedirect("you are not authorized ")
    if request.method =="POST":
        hotel_name=request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request,"Hotel Details Updated ")
        return HttpResponseRedirect(request.path_info)

    # Retrieve amenities for rendering in the template
    ameneties = Ameneties.objects.all()
    
    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties})



def logout_view(request):
    logout(request)
    messages.warning(request,"Yor are loged Out  ")
    return redirect('/accounts/login/')


def booking_details(request):
    return render(request,'vendor/booking_details.html')


        

    
    