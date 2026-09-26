from myportfolio.models import Project
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command inserts project data"
    def handle(self, *args, **options):
        Project.objects.all().delete()

        names = [
            'Daily QGT Status: ARS Incidents Overview 1',
            'Daily QGT Status: ARS Incidents Overview 2'    
        ]

        problem_statements = [
        'Manual tracking of daily incident metrics is time-consuming and prone to delays, making it hard to identify not-actioned incidents, aging tickets, and resolution gaps. This limits visibility for managers and increases the risk of SLA breaches.',
        'Manual tracking of daily incident metrics is time-consuming and prone to delays, making it hard to identify not-actioned incidents, aging tickets, and resolution gaps. This limits visibility for managers and increases the risk of SLA breaches.'
        ]

        business_cases = [
            'Automating daily incident reporting provides quick, accurate insights into assigned, resolved, and aging incidents. It improves efficiency, saves time, enhances SLA compliance, and supports better resource allocation, leading to improved customer satisfaction and reduced operational costs.',
            'Automating daily incident reporting provides quick, accurate insights into assigned, resolved, and aging incidents. It improves efficiency, saves time, enhances SLA compliance, and supports better resource allocation, leading to improved customer satisfaction and reduced operational costs.'
        ]

        solutions = [
            'Python function connects to ServiceNow, fetches incident data, prepares reports, Azure Function App and Logic App schedule the workflow, and GitHub is used for version control and report distribution, ensuring a reliable reporting pipeline.',
            'Python function connects to ServiceNow, fetches incident data, prepares reports, Azure Function App and Logic App schedule the workflow, and GitHub is used for version control and report distribution, ensuring a reliable reporting pipeline.'
        ]

        img_urls = [
            'https://i.pinimg.com/736x/a8/08/35/a808353507aa0bd01a6812a412240758.jpg',
            'https://i.pinimg.com/736x/a8/08/35/a808353507aa0bd01a6812a412240758.jpg'    
        ]

        view_code_urls = [
            'https://picsum.photos/id/3/230/200',
            'https://picsum.photos/id/4/230/200'     
        ]

        for name, problem_statement, business_case, solution, img_url, view_code_url in zip(names, problem_statements, business_cases, solutions, img_urls, view_code_urls):
            Project.objects.create(name=name, problem_statement=problem_statement, business_case=business_case, solution=solution, img_url=img_url, view_code_url = view_code_url)

        self.stdout.write(self.style.SUCCESS("Completed Inserting Projects"))