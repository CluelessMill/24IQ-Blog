# Generated by Django 5.0.4 on 2024-04-21 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsComments",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("creation_date", models.DateField()),
                ("text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("nickname", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("info", models.TextField(default="", null=True)),
                (
                    "role",
                    models.CharField(
                        choices=[("user", "User"), ("admin", "Admin")],
                        default="user",
                        max_length=20,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "profile_img",
                    models.TextField(
                        default="/media/user-images/default.svg", null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                ("news_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(default="")),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                ("creation_date", models.DateField()),
                ("content_text", models.TextField()),
                ("main_img", models.ImageField(upload_to="news-images/")),
                ("logo_img", models.ImageField(upload_to="news-images/")),
                ("likes", models.IntegerField(default=0)),
                ("comments", models.ManyToManyField(default=[], to="api.newscomments")),
            ],
        ),
        migrations.CreateModel(
            name="Sessions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="api.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="newscomments",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.user"
            ),
        ),
    ]
