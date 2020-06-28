# Generated by Django 3.0.7 on 2020-06-28 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_auto_20200628_1755'),
        ('home', '0002_auto_20200520_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroimage',
            name='hero_image',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='hero_image',
                to='image.Image'),
        ),
        migrations.AlterField(
            model_name='portfolioimage',
            name='portfolio_image',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='portfolio_image',
                to='image.Image'),
        ),
    ]
