from myportfolio.models import Technical_Skills
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command inserts Technical_Skills data"
    def handle(self, *args, **options):
        Technical_Skills.objects.all().delete()
        skill_categories = ['Languages and Frameworks', 'Database', 'Cloud and Devops', 'Tools and Platforms']
        skills = ['Python, Django, HTML, CSS, BootStrap 5', 'MySQL', 'Azure', 'VisualStudio Code, ServiceNow']

        for skill_category, skills in zip(skill_categories, skills):
            Technical_Skills.objects.create(skill_category=skill_category, skills=skills)

        self.stdout.write(self.style.SUCCESS("Completed Inserting Skills"))