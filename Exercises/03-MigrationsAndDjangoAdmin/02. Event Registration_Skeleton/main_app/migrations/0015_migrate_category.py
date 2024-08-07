# Generated by Django 4.2.4 on 2023-10-30 20:29

from django.db import migrations


def set_category(apps,schema_editor):
    smartphone_model = apps.get_model("main_app", "Smartphone")
    smartphones = smartphone_model.objects.all()

    for smartphone in smartphones:
        if smartphone.price >= 750:
            smartphone.category = "Expensive"
        else:
            smartphone.category = "Cheap"
        smartphone.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_migrate_price'),
    ]

    operations = [
        migrations.RunPython(set_category)
    ]
