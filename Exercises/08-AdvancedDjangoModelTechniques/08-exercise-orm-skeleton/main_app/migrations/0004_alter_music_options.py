# Generated by Django 4.2.4 on 2023-11-11 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_book_movie_music'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='music',
            options={'ordering': ['-created_at', 'title'], 'verbose_name': 'Model Music', 'verbose_name_plural': 'Models of type - Music'},
        ),
    ]
