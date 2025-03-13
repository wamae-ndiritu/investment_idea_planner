from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, ProfileForm, InvestmentIdeaForm, InvestmentPlanForm, SavingForm
from .models import InvestmentIdea, InvestmentPlan, CustomUser, Saving, Notification
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
import json
from django.db.models import Q

def home(request):
    featured_ideas = InvestmentIdea.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'page': 'home', 'investment_ideas': featured_ideas})

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


def user_get_investment_ideas(request):
    investment_ideas = InvestmentIdea.objects.all()
    return render(request, 'ideas.html', {'investment_ideas': investment_ideas})


def user_get_investment_idea_details(request, idea_id):
    investment_idea = get_object_or_404(InvestmentIdea, id=idea_id)
    return render(request, 'idea_details.html', {'investment_idea': investment_idea})

@admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

@admin_required
def get_investment_ideas(request):
    investment_ideas = InvestmentIdea.objects.all()
    return render(request, 'admin/ideas.html', {'investment_ideas': investment_ideas})


@admin_required
def get_investment_idea_details(request, idea_id):
    investment_idea = get_object_or_404(InvestmentIdea, id=idea_id)
    return render(request, 'admin/idea_details.html', {'investment_idea': investment_idea})


def search_investment_ideas(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    investment_ideas = InvestmentIdea.objects.filter(
        Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
    )
    highlighted_ideas = []
    for idea in investment_ideas:
        highlighted_idea = {
            'id': idea.id,
            'title': idea.title.replace(query, f'<mark>{query}</mark>'),
            'summary': idea.summary.replace(query, f'<mark>{query}</mark>'),
            'content': idea.content.replace(query, f'<mark>{query}</mark>'),
            'price_range': idea.price_range,
            'extract_thumbnail': idea.extract_thumbnail
        }
        highlighted_ideas.append(highlighted_idea)
    if search_type == 'normal_search':
        return render(request, 'ideas.html', {'investment_ideas': highlighted_ideas, 'query': query})
    else:
        return render(request, 'admin/ideas.html', {'investment_ideas': highlighted_ideas, 'query': query})
    

@login_required(login_url='login')
def create_investment_plan(request, idea_id):
    investment_idea = get_object_or_404(InvestmentIdea, id=idea_id)
    existing_plan = InvestmentPlan.objects.filter(
        user=request.user, investment_idea=investment_idea).first()
    if request.method == 'POST':
        form = InvestmentPlanForm(request.POST)
        if form.is_valid():
            investment_plan = form.save(commit=False)
            investment_plan.user = request.user
            investment_plan.investment_idea = investment_idea
            investment_plan.save()
            form = InvestmentPlanForm(instance=investment_plan)
            messages.success(request, 'Calculations completed')
            return render(request, 'investment_plan.html', {'form': form, 'investment_idea': investment_idea, 'step': 1, 'calculations': {
                'id': investment_plan.id,
                'expected_investment_amount': investment_plan.target_amount,
                'number_of_months': investment_plan.get_no_of_months(),
                'salary': investment_plan.salary,
                'monthly_savings': investment_plan.get_monthly_savings()
            }})
        else:
            errors = json.loads(form.errors.as_json())
            for msg in errors:
                messages.error(request, f"{msg}: {errors[msg][0]['message']}")
    else:
        form = InvestmentPlanForm()
        if existing_plan:
            messages.info(
                request, 'You already have an investment plan for this idea. Please view your existing plan.')
            return redirect('view_investment_plan', plan_id=existing_plan.id)
    return render(request, 'investment_plan.html', {'form': form, 'investment_idea': investment_idea, 'step': 1})

@login_required(login_url='login')
def set_savings_reminder(request, plan_id):
    investment_plan = get_object_or_404(InvestmentPlan, id=plan_id)
    dates = [day for day in range(1, 32)]
    form = InvestmentPlanForm(instance=investment_plan)
    if request.method == 'POST':
        is_notification_enabled = request.POST.get('reminders', 'off')
        salary_date = request.POST.get('salary_date')
        if is_notification_enabled == 'off':
            investment_plan.is_notification_enabled = False
            investment_plan.save()
            messages.warning(request, 'Automatic reminders disabled')
        else:
            investment_plan.is_notification_enabled = True
            investment_plan.notification_time = salary_date
            investment_plan.save()
            messages.success(request, 'Automatic reminders enabled')
        return render(request, 'investment_plan.html', {'form': form, 'investment_idea': investment_plan.investment_idea, 'step': 3, 'days': dates, 'investment_plan': investment_plan})
    else:
        return render(request, 'investment_plan.html', {'form': form, 'investment_idea': investment_plan.investment_idea, 'step': 2, 'days': dates, 'investment_plan': investment_plan})

@login_required(login_url='login')
def list_investment_plans(request):
    investment_plans = InvestmentPlan.objects.filter(user=request.user)
    return render(request, 'investment_plans.html', {'investment_plans': investment_plans})

@login_required(login_url='login')
def view_investment_plan(request, plan_id):
    investment_plan = get_object_or_404(InvestmentPlan, id=plan_id)
    if request.method == 'POST':
        form = SavingForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.investment_plan = get_object_or_404(InvestmentPlan, id=plan_id)
            saving.save()
            messages.success(request, 'Saving recorded successfully')
            return redirect('view_investment_plan', plan_id=plan_id)
        else:
            errors = json.loads(form.errors.as_json())
            for msg in errors:
                messages.error(request, f"{msg}: {errors[msg][0]['message']}")
    else:
        return render(request, 'plan_details.html', {'investment_plan': investment_plan, 'savings': Saving.objects.filter(investment_plan=investment_plan).order_by('-id')})
    

@admin_required
def create_investment_idea(request):
    form = InvestmentIdeaForm()
    if request.method == 'POST':
        form = InvestmentIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment idea added successfully')
            return redirect('admin_investment_ideas')
        else:
            errors = json.loads(form.errors.as_json())
            for msg in errors:
                messages.error(request, f"{msg}: {errors[msg][0]['message']}")
    else:
        form = InvestmentIdeaForm()
    return render(request, 'admin/idea_form.html', {'form': form})


@admin_required
def edit_investment_idea(request, idea_id):
    investment_idea = get_object_or_404(InvestmentIdea, id=idea_id)
    if request.method == 'POST':
        form = InvestmentIdeaForm(request.POST, request.FILES, instance=investment_idea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment idea updated successfully')
            return redirect('admin_investment_ideas')
        else:
            errors = json.loads(form.errors.as_json())
            for msg in errors:
                messages.error(request, f"{msg}: {errors[msg][0]['message']}")
    else:
        form = InvestmentIdeaForm(instance=investment_idea)
    return render(request, 'admin/idea_form.html', {'form': form, 'type': 'edit'})

@admin_required
def delete_investment_idea(request, idea_id):
    cancel_url = request.session.get('cancel_url', request.META.get('HTTP_REFERER', 'admin_investment_ideas'))
    investment_idea = get_object_or_404(InvestmentIdea, id=idea_id)
    if request.method == 'POST':
        investment_idea.delete()
        messages.success(request, 'Investment idea deleted successfully')
        return redirect('admin_investment_ideas')
    else:
        request.session['cancel_url'] = cancel_url
        return render(request, 'admin/delete.html', {'description': investment_idea.title, 'id': idea_id, 'cancel_url': cancel_url})
    

@admin_required
def get_users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/users.html', {'users': users})
