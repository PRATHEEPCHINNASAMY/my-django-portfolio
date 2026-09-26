
from django.contrib import admin
from .models import Project, Aboutme

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'problem_statement')
    search_fields = ('name', 'problem_statement')
    list_filter = ('name',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Aboutme)