# Generated by Django 5.1.2 on 2024-10-22 16:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_alter_statusmessage_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img_url',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.statusmessage')),
            ],
        ),
    ]