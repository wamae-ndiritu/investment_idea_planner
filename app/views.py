from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, ProfileForm, InvestmentIdeaForm, InvestmentPlanForm, SavingForm
from .models import InvestmentIdea, InvestmentPlan, CustomUser, Saving, Notification
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def register(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed up successfully')
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
        import json
        errors = json.loads(form.errors.as_json())
        for msg in errors:
            messages.error(request, f"{msg}: {errors[msg][0]['message']}")
        return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'register.html', {'form': form})


def login_user(request):
    user = request.user
    return_url = request.GET.get('next')
    if user.is_authenticated:
        if return_url is not None:
            return HttpResponseRedirect(return_url)
        return redirect('home')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        print("Logged in user: ", user)
        login(request, user)
        messages.success(request, 'Signed in successfully')
        return_url = request.POST.get('return_url', None)
        if return_url and return_url != 'None':
            return HttpResponseRedirect(return_url)
        else:
            return redirect('home')
    else:
        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html', {'return_url': return_url})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})

@admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

@admin_required
def get_investment_ideas(request):
    investment_ideas = InvestmentIdea.objects.all()
    return render(request, 'admin/ideas.html', {'investment_ideas': investment_ideas})

@admin_required
def create_investment_idea(request):
    form = InvestmentIdeaForm()
    if request.method == 'POST':
        form = InvestmentIdeaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment idea added successfully')
            return redirect('investment_idea')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = InvestmentIdeaForm()
    return render(request, 'admin/idea_form.html', {'form': form})

@admin_required
def get_users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/users.html', {'users': users})
