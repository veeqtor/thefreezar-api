# Generated by Django 3.0.6 on 2020-05-20 12:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('image', '0002_image_is_hero_bg'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioImage',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by',
                 models.CharField(blank=True, max_length=200, null=True)),
                ('updated_by',
                 models.CharField(blank=True, max_length=200, null=True)),
                ('portfolio_description',
                 models.CharField(blank=True,
                                  max_length=20,
                                  null=True,
                                  verbose_name='Hero Caption')),
                ('portfolio_image_url',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='image.Image')),
            ],
            options={
                'verbose_name_plural': 'Portfolio Images',
                'db_table': 'portfolio_images',
            },
        ),
        migrations.CreateModel(
            name='HeroImage',
            fields=[
                ('id',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by',
                 models.CharField(blank=True, max_length=200, null=True)),
                ('updated_by',
                 models.CharField(blank=True, max_length=200, null=True)),
                ('hero_caption',
                 models.CharField(max_length=20, verbose_name='Hero Caption')),
                ('hero_image_url',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='image.Image')),
            ],
            options={
                'verbose_name_plural': 'Hero Images',
                'db_table': 'hero_images',
            },
        ),
    ]
