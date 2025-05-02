from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm, NotificationPreferencesForm
from .models import User, UserProfile
from reports.models import CrimeReport
from safecircles.models import SafeCircle

# Create your views here.

def home(request):
    stats = {
        'users': User.objects.count(),
        'circles': SafeCircle.objects.count(),
        'reports': CrimeReport.objects.count(),
        'resolved': CrimeReport.objects.filter(status='resolved').count(),
    }
    return render(request, 'core/home.html', {'stats': stats})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'core/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def notification_preferences(request):
    if request.method == 'POST':
        form = NotificationPreferencesForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated!')
            return redirect('users:notification_preferences')
    else:
        form = NotificationPreferencesForm(instance=request.user.profile)
    
    return render(request, 'core/notification_preferences.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    recent_activity = []  # Will be implemented with activity tracking
    emergency_contacts = {
        'name': profile.emergency_contact_name,
        'phone': profile.emergency_contact_phone
    }
    
    return render(request, 'core/dashboard.html', {
        'user': user,
        'profile': profile,
        'recent_activity': recent_activity,
        'emergency_contacts': emergency_contacts
    })

def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})
