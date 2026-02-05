from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.urls import reverse
from twilio.rest import Client
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Vendor, ProductTracking
import uuid

def vendor_register(request):
    if request.method == 'POST':
        # Create user and vendor
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            vendor = Vendor.objects.create(
                user=user,
                company_name=request.POST['company_name'],
                phone=request.POST['phone'],
                tracking_id=f"VEN-{uuid.uuid4().hex[:8].upper()}"
            )
            
            # Send verification email
            token = get_random_string(32)
            # Store token in session or DB
            send_verification_email(user.email, token)
            
            return redirect('verify_email')
    else:
        user_form = UserCreationForm()
    
    return render(request, 'vendors/register.html', {'form': user_form})

def send_verification_email(email, token):
    verify_url = f"http://localhost:8000/verify/{token}/"
    send_mail(
        'Verify Your Vendor Account',
        f'Click here to verify: {verify_url}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')
    
    vendors = Vendor.objects.all()
    trackings = ProductTracking.objects.all()
    return render(request, 'admin/dashboard.html', {
        'vendors': vendors, 
        'trackings': trackings
    })

def update_tracking_status(request, tracking_id):
    if not request.user.is_staff:
        return redirect('login')
    
    tracking = ProductTracking.objects.get(tracking_id=tracking_id)
    tracking.status = request.POST['status']
    tracking.save()
    
    # Send SMS to vendor
    send_sms_to_vendor(tracking.vendor.phone, tracking)
    
    return redirect('admin_dashboard')

def send_sms_to_vendor(phone, tracking):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Tracking Update: {tracking.product_name} - {tracking.status.upper()}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=str(phone)
    )
