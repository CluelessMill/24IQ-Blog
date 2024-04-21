# Generated by Django 5.0.4 on 2024-04-21 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_email_alter_user_nickname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newscomments',
            name='author',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='id',
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField()),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(default='')),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateField()),
                ('content_text', models.TextField()),
                ('main_img', models.ImageField(upload_to='post-images/')),
                ('logo_img', models.ImageField(upload_to='post-images/')),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.ManyToManyField(default=[], to='api.postcomments')),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.DeleteModel(
            name='NewsComments',
        ),
    ]
