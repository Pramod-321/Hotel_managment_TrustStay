import uuid
from django.core.mail import send_mail
from  django.conf import settings
from django.utils.text import slugify
from home.models import Hotel 

def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email,token):
    subject="Verify your Email Address"
    message=f"""Hi this is OYO , Please verify your email account by clicking 
                THis Link 
                http://127.0.0.1:8000/accounts/verify-account/{token}
                """
    
    
    
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )    
 
 

  
def sendOTPtoEmail(email,otp):
    subject="OYO"
    message=f"""Hi this is OYO , OTP for your account to login
                THis Link
                 
                {otp}
                
                """
    
    
    
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )    
    
def generateSlug(hotel_name):
    slug=f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generateSlug(hotel_name)

    return slug