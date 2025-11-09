# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz_events_app', '0003_alter_useranswer_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubmission',
            name='user_name',
        ),
        migrations.AddField(
            model_name='usersubmission',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]