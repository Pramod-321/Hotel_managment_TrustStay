from django.urls import path
from accounts import views
urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register,name='register'),
    path('login_vendor/',views.login_vendor,name='login_vendor'),
    path('register_vendor/',views.register_vendor,name='register_vendor'),
    path('vendor_dashboard/',views.vendor_dashboard,name='vendor_dashboard'),
    path('send_otp/<email>/',views.send_otp,name='send_otp'),
    path('verify-otp/<email>/', views.verify_otp, name='verify-otp'),
    path('verify-account/<token>/',views.verify_email_token,name='verify_email_token'),
    path('add_hotel/', views.add_hotel , name="add_hotel"),
    path('<slug>/upload_image/', views.upload_image , name="upload_image"),
    path('delete_image/<int:id>/', views.delete_image , name="delete_image"),
    path('edit-hotel/<slug>/',views.edit_hotel,name="edit_hotel"),
    path('logout/' , views.logout_view , name="logout_view"),
    path('booking_detils/',views.booking_details,name="booking_detils"),
]
