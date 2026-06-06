from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm, CustomLoginForm
from .models import UserProfile


def register_view(request):
    """Handle student registration."""
    if request.user.is_authenticated:
        return redirect('quiz_dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created successfully.')
            return redirect('quiz_dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('quiz_dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Redirect lecturers to admin dashboard
            if hasattr(user, 'profile') and user.profile.is_lecturer:
                return redirect('admin_dashboard')
            return redirect('quiz_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """Display user profile."""
    user = request.user
    attempts = user.quiz_attempts.all()
    context = {
        'user': user,
        'profile': user.profile,
        'attempts': attempts,
        'total_attempts': attempts.count(),
    }
    return render(request, 'accounts/profile.html', context)
