from myportfolio.models import Skills
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command inserts skills data"

    def handle(self, *args, **options):
        Skills.objects.all().delete()
        skill_names = ['HTML', 'CSS', 'Bootstrap', 'Python', 'MySQL', 'Djano']
        percentages = ['65', '70', '75', '80', '85', '90']

        for skill_name, percentage in zip(skill_names, percentages):
            Skills.objects.create(skill_name=skill_name, percentage=percentage)
        
        self.stdout.write(self.style.SUCCESS("Completed Inserting Skills"))