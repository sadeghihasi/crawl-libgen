# Generated by Django 4.2.10 on 2024-02-24 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "keyword",
                    models.CharField(max_length=50, verbose_name="searched word"),
                ),
                (
                    "author_name",
                    models.CharField(max_length=255, verbose_name="auther name"),
                ),
                (
                    "file_address",
                    models.FileField(
                        upload_to="C:\\Users\\Hasan\\Documents\\projects\\freelancer\\python/uploads/",
                        verbose_name="downloal address",
                    ),
                ),
                ("file", models.FileField(upload_to="")),
                (
                    "id",
                    models.CharField(
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="id",
                    ),
                ),
                ("hash", models.CharField(max_length=32)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
