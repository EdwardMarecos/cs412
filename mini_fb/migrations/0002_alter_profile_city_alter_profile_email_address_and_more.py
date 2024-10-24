# Generated by Django 5.1.1 on 2024-10-15 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email_address',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_img_url',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='StatusMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('message', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.profile')),
            ],
        ),
    ]