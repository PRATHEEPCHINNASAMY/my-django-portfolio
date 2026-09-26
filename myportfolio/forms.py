from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from myportfolio.models import Project, Skills, Technical_Skills, Professional_Experience
from datetime import datetime

class ContactForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100, required=True)
    email = forms.EmailField(label="Your Email", required=True)
    subject = forms.CharField(label="Subject", required=True)
    message = forms.CharField(label="Message", required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")

        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError("Passwords do not match!")

from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100, required=True)
    password = forms.CharField(label="Password", max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email and password!")
            
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("No user registered with this email!")
        return cleaned_data
    
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", max_length=100, required=True)
    confirm_password = forms.CharField(label="Confirm Password", max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password!=confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
class ProjectForm(forms.ModelForm):
    name = forms.CharField(label="Project Name", max_length=100, required=True)
    problem_statement = forms.CharField(label="Problem Statement", max_length=1000, required=True)
    business_case = forms.CharField(label="Business Case", max_length=1000, required=True)
    solution = forms.CharField(label="solution", max_length=1000, required=True)
    view_code_url = forms.CharField(label="View Code URL", max_length=100, required=True)

    class Meta:
        model =  Project
        fields = ['name', 'problem_statement', 'business_case', 'solution', 'view_code_url']
    
    def clean(self):
        cleaned_data =  super().clean()
        name = cleaned_data.get('name')
        problem_statement = cleaned_data.get('problem_statement')
        business_case = cleaned_data.get('business_case')
        solution = cleaned_data.get('solution')
        view_code_url = cleaned_data.get('view_code_url')

        # Custom Validation
        if name and len(name)<5:
            raise forms.ValidationError('Project Name must be at least 5 characters long.')
        if view_code_url and len(view_code_url)<10:
            raise forms.ValidationError('View Code URL must be at least 10 characters long.')
        return cleaned_data
    
class SkillForm(forms.ModelForm):
    skill_name = forms.CharField(label="Skill Name" ,max_length=100, required=True)
    percentage = forms.IntegerField(label="Percentage", required=True)

    class Meta:
        model = Skills
        fields = ['skill_name', 'percentage']
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class TechnicalSkillForm(forms.ModelForm):
    skill_category = forms.CharField(label="Technical Skill Category", max_length=100, required=True)
    skills = forms.CharField(label="Skills", max_length=100, required=True)

    class Meta:
        model = Technical_Skills
        fields = ['skill_category', 'skills']

    def clean(self):
        cleaned_data =  super().clean()
        return cleaned_data

class ProfessionalExperienceForm(forms.ModelForm):
    role = forms.CharField(label="Role", max_length=100, required=True)
    company_name = forms.CharField(label="Company Name", max_length=100, required=True)
    location = forms.CharField(label="Location", max_length=100, required=True)
    joining_date = forms.DateField(label="Joining Date", required=True, input_formats=["%Y-%m"])
    leaving_date = forms.DateField(label="Leaving Date", required=False, input_formats=["%Y-%m"])
    details = forms.CharField(label="Details", required=True)
    class Meta:
        model = Professional_Experience
        fields = ['role', 'company_name', 'location', 'joining_date', 'leaving_date', 'details']

    def clean(self):
        cleaned_data =  super().clean()
        return cleaned_data
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(required=True)
    def clean(self):
        cleaned_data =  super().clean()
        return cleaned_data