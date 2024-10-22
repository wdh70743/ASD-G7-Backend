import os
import sys
import django

# Add the parent directory of 'taskmanager' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from project.models import Project
from task.models import Task
from users.models import User

from datetime import datetime, timedelta
User_obj = get_user_model()

SUPERUSER_EMAIL = 'admin@admin.com'
SUPERUSER_USERNAME = 'admin1234'
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

idx = 1
for project_data in project_list:
    owner = User.objects.get(id=idx)
    Project.objects.create(owner=owner,
                           projectname=project_data[0],
                           description=project_data[1],
                           start_date=project_data[2],
                           end_date=project_data[3],
                           priority=project_data[4]
                           )
    idx += 1
owner_1 = User.objects.get(id=1)
owner_2 = User.objects.get(id=2)
owner_3 = User.objects.get(id=3)
project_1 = Project.objects.get(id=1)
project_2 = Project.objects.get(id=2)
project_3 = Project.objects.get(id=3)
current_date = datetime.now().date()

Task.objects.create(
    owner=owner_1,
    project=project_1,
    priority="High",
    status=False,
    title="Design Homepage Layout",
    description="Redesign the company website for better user experience.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_1,
    project=project_1,
    priority="High",
    status=False,
    title="Setup Color Scheme",
    description="Finalize the color scheme based on the company's branding.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_1,
    project=project_1,
    priority="High",
    status=False,
    title="Implement Mobile Responsive Design",
    description="Ensure the website is fully responsive across all devices.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)

Task.objects.create(
    owner=owner_2,
    project=project_2,
    priority="High",
    status=False,
    title="Build App Prototype",
    description="Create the initial prototype of the mobile app.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_2,
    project=project_2,
    priority="High",
    status=False,
    title="Setup Backend API",
    description="Set up the backend API for the mobile app's functionality.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_2,
    project=project_2,
    priority="High",
    status=False,
    title="Test App on Devices",
    description="Test the mobile app on different devices for compatibility.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)

Task.objects.create(
    owner=owner_3,
    project=project_3,
    priority="High",
    status=False,
    title="Analyze Legacy Data",
    description="Review legacy system data and create a migration strategy.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_3,
    project=project_3,
    priority="High",
    status=False,
    title="Create Migration Scripts",
    description="Develop scripts to automate data migration from legacy systems.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
Task.objects.create(
    owner=owner_3,
    project=project_3,
    priority="High",
    status=False,
    title="Validate Migrated Data",
    description="Ensure all data is correctly migrated and validated.",
    start_date=current_date - timedelta(days=7),
    due_date=current_date
)
