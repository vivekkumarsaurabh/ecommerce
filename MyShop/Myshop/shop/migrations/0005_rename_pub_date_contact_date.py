# Generated by Django 4.0.3 on 2022-04-07 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_contact_mobile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='pub_date',
            new_name='date',
        ),
    ]
