# Generated by Django 5.1 on 2024-10-02 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_project_owner'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', to='users.user'),
        ),
    ]
