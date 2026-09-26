from django.shortcuts import get_object_or_404, render, redirect
from django.http import  HttpResponse
from django.urls import reverse
import logging
from .models import Professional_Experience, Project, Aboutme, Skills, Technical_Skills
from django.http import Http404
from .forms import ContactForm, ForgotPasswordForm, LoginForm, ProfessionalExperienceForm, ProjectForm, RegisterForm, ResetPasswordForm, SkillForm, TechnicalSkillForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
# Create your views here.

# projects = [
#     {'id': 1, 'name' : 'Daily QGT Status: ARS Incidents Overview 1', 'created_at' : 'July 19, 2026'},
#     {'id': 2, 'name' : 'Daily QGT Status: ARS Incidents Overview 2', 'created_at' : 'July 19, 2026'},
#     {'id': 3, 'name' : 'Daily QGT Status: ARS Incidents Overview 3', 'created_at' : 'July 19, 2026'},
#     {'id': 4, 'name' : 'Daily QGT Status: ARS Incidents Overview 4', 'created_at' : 'July 19, 2026'},
    
#     ]


@never_cache
@login_required
def home(request):
    portfolio_title = "PyCraftbyPradeep"
    Aboutme_Content = Aboutme.objects.first()
    skills = Skills.objects.all()
    technical_skills = Technical_Skills.objects.all()
    professional_experience = Professional_Experience.objects.all()
    projects = Project.objects.all()
    if Aboutme_Content is None or not Aboutme_Content.content:
        Aboutme_Content = "Web Developer and Automation Engineer with experience building responsive front end for web applications and developing Python automation tools deployed via Azure and GitHUB Actions. Skilled in front-end development using HTML, CSS, and Bootstrap with backend integration using Python and MySQL. Successfully integrated ServiceNow platforms and reduce manual workload by up to 80% through automation. Known for writing clean, maintainable code, improving system stability by 30%, and independently delivering solutions that align with business objectives."
    else:
        Aboutme_Content = Aboutme_Content.content
    if request.method=="POST":
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        logger = logging.getLogger("Testing")
        if form.is_valid():            
            logger.debug(f'Form data is {form.cleaned_data['name']}, {form.cleaned_data['email']}, {form.cleaned_data['subject']}, {form.cleaned_data['message']}')
            html_message = render_to_string(
                'myportfolio/contact_email.html',
                {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message,
                }
            )

            send_mail(
                subject=f"Contact Form: {subject}",
                message=f"New message from {name} ({email}):\n\n{message}",
                from_email=None,
                recipient_list=['pycraftbypradeep@gmail.com'],
                html_message=html_message,
            )
            success_message = "Your Email Has Been Sent Successfully!"
            return render(request, 'myportfolio/home.html', {'portfolio_title':portfolio_title, 'Aboutme_Content':Aboutme_Content, 'skills':skills, 'technical_skills':technical_skills, 'professional_experience':professional_experience, 'projects':projects, 'form':form, 'success_message':success_message})
        else:
            logger.debug("Form submission failed")
            return render(request, 'myportfolio/home.html', {'portfolio_title':portfolio_title, 'Aboutme_Content':Aboutme_Content, 'skills':skills, 'technical_skills':technical_skills, 'professional_experience':professional_experience, 'projects':projects, 'form':form, 'name':name, 'email':email, 'subject':subject, 'message':message})
    return render(request, 'myportfolio/home.html', {'portfolio_title':portfolio_title, 'projects':projects, 'Aboutme_Content':Aboutme_Content, 'skills':skills, 'technical_skills':technical_skills, 'professional_experience':professional_experience})
@login_required
def details(request, slug):
    if request.user and not request.user.has_perm('myportfolio.view_project'):
        messages.error( request, "You have no permission to view any projects!")
        return redirect(f"{reverse('myportfolio:home')}#portfolio")    
    projects = Project.objects.all()
    # project = next((item for item in projects if item['id'] == int(project_id)), None)
    try:
        project = Project.objects.get(slug=slug)
        logger = logging.getLogger("Testing")
        logging.debug(f'Project variable is {project}')
    except Project.DoesNotExist:
        raise Http404("Project Does Not Exist!")
    return render(request, 'myportfolio/details.html', {'project':project})

def register(request):    
    form = RegisterForm(request.POST)
    name = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    success_message = ""
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Add user to readers group
            readers_group, created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request, "Registration successful! Please login.")
            return redirect("myportfolio:login")
    else:
        form = RegisterForm()
          
    return render(request, "myportfolio/register.html", {'form':form, 'name':name, 'email':email, 'password':password, 'confirm_password':confirm_password})


def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Logged in success!")
                return redirect("myportfolio:home")
    return render(request, "myportfolio/login.html", {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('myportfolio:login')

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            # send password reset  link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('myportfolio/reset_password_email.html', {
                'domain':domain,
                'uid':uid,
                'token':token,
                }
                )
            send_mail( subject, "Please use an HTML-compatible email client to reset your password.",  None, [email], html_message=message )
            messages.success(request, 'Email has been sent!')
    return render(request, 'myportfolio/forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password reset has been done successfully!")
                return redirect("myportfolio:login")
            else:
                messages.error(request, 'The password reset link is invalid!')
    return render(request, "myportfolio/reset_password.html", {'form':form})
@login_required
@permission_required('myportfolio.add_project', raise_exception=True)
def new_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)        
        if form.is_valid():            
            project = form.save()
            messages.success(request, "Project Added successfully!")
            return redirect(f"{reverse('myportfolio:home')}#portfolio")
    return render(request, 'myportfolio/new_project.html', {'form':form})
@login_required
@permission_required('myportfolio.change_project', raise_exception=True)
def edit_project(request, project_id):
    if request.user and not request.user.has_perm('myportfolio.change_project'):
        messages.error( request, "You have no permission to update any projects!")
        return redirect(f"{reverse('myportfolio:home')}#portfolio")      
    form = ProjectForm()
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)        
        if form.is_valid():            
            project = form.save()
            messages.success(request, "Project Updated successfully!")
            return redirect(f"{reverse('myportfolio:home')}#portfolio")
    return render(request, 'myportfolio/edit_project.html', {'form':form, 'project':project})
@login_required
def delete_project(request, project_id):
    if request.user and not request.user.has_perm('myportfolio.delete_project'):
        messages.error( request, "You have no permission to delete any projects!")
        return redirect(f"{reverse('myportfolio:home')}#portfolio")
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project Deleted successfully!")
    return redirect(f"{reverse('myportfolio:home')}#portfolio")
@login_required
@permission_required('myportfolio.publish_project', raise_exception=True)
def publish_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_published = True
    project.save()
    messages.success(request, "Project Published successfully!")
    return redirect(f"{reverse('myportfolio:home')}#portfolio")
@login_required
@permission_required('myportfolio.add_project', raise_exception=True)
def new_skill(request):
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, "Skill Added successfully!")
            return redirect(f"{reverse('myportfolio:home')}#about")
    return render(request, 'myportfolio/new_skill.html', {'form':form})
@login_required
@permission_required('myportfolio.change_project', raise_exception=True)
def edit_skill(request, skill_id):
    if request.user and not request.user.has_perm('myportfolio.change_project'):
        messages.error( request, "You have no permission to edit any skills!")
        return redirect(f"{reverse('myportfolio:home')}#about")
    form = SkillForm()
    skill = get_object_or_404(Skills, id=skill_id)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)        
        if form.is_valid():            
            skill = form.save()
            messages.success(request, "Skill Updated successfully!")
            return redirect(f"{reverse('myportfolio:home')}#about")
    return render(request,'myportfolio/edit_skill.html', {"form":form, "skill":skill})
@login_required
def delete_skill(request, skill_id):
    if request.user and not request.user.has_perm('myportfolio.delete_project'):
        messages.error( request, "You have no permission to delete any skills!")
        return redirect(f"{reverse('myportfolio:home')}#about")
    skill = get_object_or_404(Skills, id=skill_id)
    skill.delete()
    messages.success(request, "Skill Deleted successfully!")
    return redirect(f"{reverse('myportfolio:home')}#about")
@login_required
@permission_required('myportfolio.add_project', raise_exception=True)
def new_technical_skill(request):
    form = TechnicalSkillForm()
    if request.method == "POST":
        form = TechnicalSkillForm(request.POST)
        if form.is_valid():
            technical_skill = form.save()
            messages.success(request, "Technical Skill Added successfully!")
            return redirect(f"{reverse('myportfolio:home')}#resume")
    return render(request, 'myportfolio/new_technical_skill.html', {'form': form})
@login_required
@permission_required('myportfolio.change_project', raise_exception=True)
def edit_technical_skill(request, technical_skill_id):
    form = TechnicalSkillForm()
    technical_skill = get_object_or_404(Technical_Skills, id=technical_skill_id)
    if request.method == "POST":
        form = TechnicalSkillForm(request.POST, instance=technical_skill)
        if form.is_valid():
            technical_skill = form.save()
            messages.success(request, "Technical Skill Updated successfully!")
            return redirect(f"{reverse('myportfolio:home')}#resume")
    return render(request, 'myportfolio/edit_technical_skill.html', {'form': form, 'technical_skill':technical_skill})
@login_required
def delete_technical_skill(request, technical_skill_id):
    if request.user and not request.user.has_perm('myportfolio.delete_project'):
        messages.error( request, "You have no permission to delete any technical skills!")
        return redirect(f"{reverse('myportfolio:home')}#resume")
    skill = get_object_or_404(Technical_Skills, id=technical_skill_id)
    skill.delete()
    messages.success(request, "Skill Deleted successfully!")
    return redirect(f"{reverse('myportfolio:home')}#resume")
@login_required
@permission_required('myportfolio.add_project', raise_exception=True)
def new_professional_experience(request):
    form = ProfessionalExperienceForm()
    if request.method == "POST":
        form = ProfessionalExperienceForm(request.POST)
        if form.is_valid():
            professional_experience = form.save()
            messages.success(request, "Porfessional Experience Added successfully!")
            return redirect(f"{reverse('myportfolio:home')}#resume")

    return render(request, 'myportfolio/new_professional_experience.html', {'form': form})
@login_required
@permission_required('myportfolio.change_project', raise_exception=True)
def edit_professional_experience(request, prof_exp_id):
    form = ProfessionalExperienceForm()
    professional_experience = get_object_or_404(Professional_Experience, id=prof_exp_id)
    if request.method == "POST":
        form = ProfessionalExperienceForm(request.POST, instance=professional_experience)
        if form.is_valid():
            professional_experience = form.save()
            messages.success(request, "Porfessional Experience Updated successfully!")
            return redirect(f"{reverse('myportfolio:home')}#resume")
    return render(request, 'myportfolio/edit_professional_experience.html', {'form': form, 'professional_experience':professional_experience})
@login_required
def delete_professional_experience(request, prof_exp_id):
    if request.user and not request.user.has_perm('myportfolio.delete_project'):
        messages.error( request, "You have no permission to delete any professional experience!")
        return redirect(f"{reverse('myportfolio:home')}#resume")
    professional_experience = get_object_or_404(Professional_Experience, id=prof_exp_id)
    professional_experience.delete()
    messages.success(request, "Professional Experience Deleted successfully!")
    return redirect(f"{reverse('myportfolio:home')}#resume")