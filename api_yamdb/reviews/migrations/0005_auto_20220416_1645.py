# Generated by Django 2.2.16 on 2022-04-16 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220416_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='confirmation_code',
            new_name='token',
        ),
    ]
