# Generated by Django 5.1 on 2024-10-22 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0005_remove_task_task_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskfile",
            name="file_name",
        ),
    ]