# Generated by Django 5.1 on 2024-08-24 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0007_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='default_things/default_profile_image.jpg', upload_to='profile_pictures'),
        ),
    ]
