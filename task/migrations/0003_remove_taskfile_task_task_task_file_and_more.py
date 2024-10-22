# Generated by Django 5.1 on 2024-10-22 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0002_alter_taskfile_file_uri"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskfile",
            name="task",
        ),
        migrations.AddField(
            model_name="task",
            name="task_file",
            field=models.ManyToManyField(
                related_name="files_tasks", to="task.taskfile"
            ),
        ),
        migrations.DeleteModel(
            name="TaskComment",
        ),
    ]