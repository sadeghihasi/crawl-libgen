# Generated by Django 4.2.10 on 2024-02-25 03:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("libgen", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="file",
        ),
        migrations.AlterField(
            model_name="book",
            name="file_address",
            field=models.FileField(
                upload_to="C:\\Users\\Hasan\\Documents\\projects\\freelancer\\python\\uploads",
                verbose_name="downloal address",
            ),
        ),
    ]
