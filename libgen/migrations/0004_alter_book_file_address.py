# Generated by Django 4.2.10 on 2024-02-27 03:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("libgen", "0003_alter_book_author_name_alter_book_file_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="file_address",
            field=models.FileField(
                max_length=255,
                upload_to="C:\\Users\\Hasan\\Documents\\projects\\freelancer\\python\\p1\\uploads",
                verbose_name="download address",
            ),
        ),
    ]
