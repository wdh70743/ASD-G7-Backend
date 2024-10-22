
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskfile',
            name='file_uri',
            field=models.FileField(upload_to='task_files/', verbose_name='file_uri'),
        ),
    ]
