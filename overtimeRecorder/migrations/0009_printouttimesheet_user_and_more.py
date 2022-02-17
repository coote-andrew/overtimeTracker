# Generated by Django 4.0.1 on 2022-02-13 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('overtimeRecorder', '0008_profile_oktoshareovertime_profile_oktoshareroster'),
    ]

    operations = [
        migrations.AddField(
            model_name='printouttimesheet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='okToShareOvertime',
            field=models.BooleanField(default=False, help_text='by ticking this box you agree to share your overtime requests with other users of this website', verbose_name='Share overtime with other users'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='okToShareRoster',
            field=models.BooleanField(default=False, help_text='by ticking this box you agree to share your roster with other users of this website', verbose_name='Share roster with other users'),
        ),
    ]
