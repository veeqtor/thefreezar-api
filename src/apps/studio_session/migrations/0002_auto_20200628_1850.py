# Generated by Django 3.0.7 on 2020-06-28 17:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studio_session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studiosessionreservation',
            name='session',
        ),
        migrations.AddField(
            model_name='studiosessionreservation',
            name='session_type',
            field=models.ForeignKey(
                default='70b1b3f7-4c80-4240-8761-b234593339ea',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='session_type',
                to='studio_session.StudioSessionType'),
            preserve_default=False,
        ),
    ]
