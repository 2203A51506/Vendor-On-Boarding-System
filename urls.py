from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendors.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
