import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

User = get_user_model()

SUPERUSER_EMAIL = 'admin@admin.com'
SUPERUSER_USERNAME = 'admin'
SUPERUSER_PASSWORD = '1234'

if not User.objects.filter(email=SUPERUSER_EMAIL).exists():
    User.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD
    )
    print(f'Superuser {SUPERUSER_USERNAME} created successfully.')
else:
    print(f'Superuser with email {SUPERUSER_EMAIL} already exists.')
