# Generated by Django 3.1.2 on 2022-03-12 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_postitem_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentitem',
            name='username',
        ),
    ]