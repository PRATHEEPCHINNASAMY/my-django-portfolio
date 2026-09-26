from myportfolio.models import Professional_Experience
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command inserts Professional_Skills data"

    def handle(self, *args, **options):        
        roles = ['Python Automation Engineer']
        company_names = ['TATA Consultancy Services']
        locations = ['Siruseri, Chennai']
        joining_dates =  ['2020-01-01']
        leaving_dates = [None]
        detail = [
"""Engineered Python automation tools, reducing report generation time by 60%.
Automated ServiceNow workflows, minimizing manual effort by 80%.
Deployed automation scripts in Azure using GitHub Actions with 99% uptime.
Improved data accuracy and tracking efficiency by 40%.
Developed dashboards for faster root-cause analysis (20% improvement).
Resolved Azure Function and container issues, improving stability by 30%.
Monitored Azure dashboards and queues for reliable operations.
Delivered modular, maintainable code and led automation projects.
Conducted Python training sessions improving team efficiency by 25%.
Reduced incident resolution time by 15% through workflow optimization.
Enhanced logging and error handling, reducing failures by 20%."""]

        for role, company_name, location, joining_date, leaving_date, details in zip(roles, company_names, locations, joining_dates, leaving_dates, detail):
            Professional_Experience.objects.create(role=role, company_name=company_name,location=location,joining_date=joining_date,leaving_date=leaving_date, details=details)

        self.stdout.write(self.style.SUCCESS("Completed Inserting Professional Experience"))