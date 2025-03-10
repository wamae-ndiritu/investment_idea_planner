from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, InvestmentIdea, InvestmentPlan, Saving, Notification

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class InvestmentIdeaForm(forms.ModelForm):
    class Meta:
        model = InvestmentIdea
        fields = ['title', 'summary', 'content', 'price_range']

class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = ['title', 'investment_idea', 'start_date', 'end_date', 'target_amount', 'salary']


class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['amount']