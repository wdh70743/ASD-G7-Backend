from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

class Project(models.Model):
    owner = models.ForeignKey("users.User", related_name="owned_projects", on_delete=models.CASCADE)
    projectname = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.BooleanField(default=False, help_text='Indicates if the project is completed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.projectname
