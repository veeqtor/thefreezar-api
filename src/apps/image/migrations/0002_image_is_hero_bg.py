# Generated by Django 3.0.6 on 2020-05-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='is_hero_bg',
            field=models.BooleanField(default=False,
                                      verbose_name='Use as Hero Background'),
        ),
    ]
