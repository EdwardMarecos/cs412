# Generated by Django 5.1.3 on 2024-11-26 22:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_rename_image_category_graphic_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='message',
            new_name='category',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
                ('bio', models.TextField(blank=True)),
                ('profile_img_file', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('major', models.CharField(blank=True, max_length=100)),
                ('minor', models.CharField(blank=True, max_length=100)),
                ('school', models.CharField(max_length=100)),
                ('class_year', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
