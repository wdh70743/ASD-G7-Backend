import os
import django
from django.contrib.auth import get_user_model
from users.models import User
from task.models import Task
from project.models import Project
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

User_obj = get_user_model()

SUPERUSER_EMAIL = 'admin@admin.com'
SUPERUSER_USERNAME = 'admin'
SUPERUSER_PASSWORD = '1234'

if not User_obj.objects.filter(email=SUPERUSER_EMAIL).exists():
    User_obj.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD
    )
    print(f'Superuser {SUPERUSER_USERNAME} created successfully.')
else:
    print(f'Superuser with email {SUPERUSER_EMAIL} already exists.')

user_list = [
    ["Alex", "test1@test.com", "1234"],
    ["Dohun", "test2@test.com", "1234"],
    ["Jinsung", "test3@test.com", "1234"],
]
project_list = [
    ["Website Redesign", "Redesign the company website for better user experience.", "2024-11-01", "2025-01-20",
     "high"],
    ["Mobile App Development", "Develop a mobile app for the e-commerce platform.", "2024-11-01", "2025-01-20", "high"],
    ["Data Migration", "Migrate data from legacy systems to the new cloud platform.", "2024-11-01", "2025-01-20",
     "high"],
]

for user_data in user_list:
    User.objects.create(username=user_data[0], email=user_data[1], password=make_password(user_data[2]))

for idx, project_data in enumerate(project_list):
    Project.objects.create(owner__id=idx,
                           projectname=project_data[0],
                           description=project_data[1],
                           start_date=project_data[2],
                           end_date=project_data[3],
                           priority=project_data[4]
                           )
Task.objects.create(
    owner__id="1",
    project__id="1",
    priority="High",
    status="Not_completed",
    title="Design Homepage Layout",
    description="Redesign the company website for better user experience.",
    start_date="2024-10-01",
    due_date="2024-10-08"
)
Task.objects.create(
    owner__id="1",
    project__id="1",
    priority="High",
    status="Not_completed",
    title="Setup Color Scheme",
    description="Finalize the color scheme based on the company's branding.",
    start_date="2024-10-01",
    due_date="2024-10-14"
)
Task.objects.create(
    owner__id="1",
    project__id="1",
    priority="High",
    status="Not_completed",
    title="Implement Mobile Responsive Design",
    description="Ensure the website is fully responsive across all devices.",
    start_date="2024-10-01",
    due_date="2024-10-21"
)

Task.objects.create(
    owner__id="2",
    project__id="2",
    priority="High",
    status="Not_completed",
    title="Build App Prototype",
    description="Create the initial prototype of the mobile app.",
    start_date="2024-10-01",
    due_date="2024-10-08"
)
Task.objects.create(
    owner__id="2",
    project__id="2",
    priority="High",
    status="Not_completed",
    title="Setup Backend API",
    description="Set up the backend API for the mobile app's functionality.",
    start_date="2024-10-01",
    due_date="2024-10-14"
)
Task.objects.create(
    owner__id="2",
    project__id="2",
    priority="High",
    status="Not_completed",
    title="Test App on Devices",
    description="Test the mobile app on different devices for compatibility.",
    start_date="2024-10-01",
    due_date="2024-10-21"
)

Task.objects.create(
    owner__id="3",
    project__id="3",
    priority="High",
    status="Not_completed",
    title="Analyze Legacy Data",
    description="Review legacy system data and create a migration strategy.",
    start_date="2024-10-01",
    due_date="2024-10-21"
)
Task.objects.create(
    owner__id="3",
    project__id="3",
    priority="High",
    status="Not_completed",
    title="Create Migration Scripts",
    description="Develop scripts to automate data migration from legacy systems.",
    start_date="2024-10-01",
    due_date="2024-10-21"
)
Task.objects.create(
    owner__id="3",
    project__id="3",
    priority="High",
    status="Not_completed",
    title="Validate Migrated Data",
    description="Ensure all data is correctly migrated and validated.",
    start_date="2024-10-01",
    due_date="2024-10-21"
)

