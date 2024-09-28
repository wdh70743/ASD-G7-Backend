from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [

    ]
    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=50, verbose_name='username')),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('priority', models.CharField(max_length=10, choices=[
                    ('low', 'Low'),
                    ('medium', 'Medium'),
                    ('high', 'High'),
                ], default='medium')),
                ('status', models.CharField(max_length=20, choices=[
                    ('not_started', 'Not Started'),
                    ('in_progress', 'In Progress'),
                    ('completed', 'Completed'),
                    ('on_hold', 'On Hold'),
                ], default='not_started')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ]
        )
    ]