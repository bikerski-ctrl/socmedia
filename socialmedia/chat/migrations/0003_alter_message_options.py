# Generated by Django 5.0.6 on 2024-07-18 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_conversation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp']},
        ),
    ]