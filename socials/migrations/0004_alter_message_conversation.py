# Generated by Django 5.1 on 2024-09-09 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0003_remove_message__to_conversation_message_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='socials.conversation'),
        ),
    ]
