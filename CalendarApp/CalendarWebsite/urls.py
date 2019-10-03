"""CalendarWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Users import views as user_views # import User views
from django.contrib.auth import views as auth_views #Import views for authentication
from django.contrib import messages

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name = 'Calendar-profile'),
    path('register/', user_views.register, name = 'Calendar-register'),
    path('login/',  auth_views.LoginView.as_view(template_name = 'users/formBase.html', extra_context={'type':'login'}), name ='Calendar-login'),
    path('logout/',  auth_views.LogoutView.as_view(template_name = 'calendar/home.html'), name ='Calendar-logout'),
    path('', include('Calendar.urls'), name = 'Calendar-home'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/formBase.html', extra_context={'type': 'resetPassword'}), name ='password_reset'),
    path('password-reset-done', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name ='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/formBase.html', extra_context={'type': 'resetPasswordConfirm'}), name ='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name ='password_reset_complete'),
]

handler403= 'Users.views.permission_denied'

# 'messages': {% messages.success(request, f'Your account has been created! You are able to log in now!')%}