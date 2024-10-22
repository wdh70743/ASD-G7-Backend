
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
    ]
