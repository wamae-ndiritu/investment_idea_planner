from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, InvestmentIdea, InvestmentPlan, Saving, Notification
from ckeditor_uploader.widgets import CKEditorUploadingWidget

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
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = InvestmentIdea
        fields = ['title', 'summary', 'content', 'price_range']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'appearance-none border border-gray-200 rounded w-full py-2 px-3 text-gray-700 focus:outline-none mb-3', 'placeholder': 'Title'}),
            'summary': forms.Textarea(attrs={'class': 'h-16 appearance-none border border-gray-200 rounded w-full py-2 px-3 text-gray-700 focus:outline-none mb-3', 'placeholder': 'Summary', 'rows': '4'}),
            'price_range': forms.TextInput(attrs={'class': 'appearance-none border border-gray-200 rounded w-full py-2 px-3 text-gray-700 focus:outline-none my-3', 'placeholder': 'Price Range'}),
        }

class InvestmentPlanForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = ['title', 'investment_idea', 'start_date', 'end_date', 'target_amount', 'salary']


class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['amount']