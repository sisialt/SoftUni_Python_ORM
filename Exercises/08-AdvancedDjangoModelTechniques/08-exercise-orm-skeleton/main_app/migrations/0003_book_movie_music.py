# Generated by Django 4.2.4 on 2023-11-11 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_customer_email_alter_customer_website_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(5, message='Author must be at least 5 characters long')])),
                ('isbn', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(6, message='ISBN must be at least 6 characters long')])),
            ],
            options={
                'verbose_name': 'Model Book',
                'verbose_name_plural': 'Models of type - Book',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('director', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8, message='Director must be at least 8 characters long')])),
            ],
            options={
                'verbose_name': 'Model Movie',
                'verbose_name_plural': 'Models of type - Movie',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artist', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(9, message='Artist must be at least 9 characters long')])),
            ],
            options={
                'verbose_name': 'Model Music',
                'verbose_name_plural': 'Models of type - Music ',
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
    ]
