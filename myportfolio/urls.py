from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "myportfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("details/<str:slug>/", views.details, name="details"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<uidb64>/<token>", views.reset_password, name = "reset_password"),
    path("new_project/", views.new_project, name="new_project"),
    path("edit_project/<int:project_id>/", views.edit_project, name="edit_project"),
    path("delete_project/<int:project_id>/", views.delete_project, name="delete_project"),
    path("publish_project/<int:project_id>/", views.publish_project, name="publish_project"),
    path("new_skill/", views.new_skill, name="new_skill"),
    path("edit_skill/<int:skill_id>/", views.edit_skill, name="edit_skill"),
    path("delete_skill/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    path("new_technical_skill/", views.new_technical_skill, name="new_technical_skill"),
    path("edit_technical_skill/<int:technical_skill_id>/", views.edit_technical_skill, name="edit_technical_skill"),
    path("delete_technical_skill/<int:technical_skill_id>/", views.delete_technical_skill, name="delete_technical_skill"),
    path("new_professional_experience/", views.new_professional_experience, name="new_professional_experience"),
    path("edit_professional_experience/<int:prof_exp_id>/", views.edit_professional_experience, name="edit_professional_experience"),
    path("delete_professional_experience/<int:prof_exp_id>/", views.delete_professional_experience, name="delete_professional_experience"),
   
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
