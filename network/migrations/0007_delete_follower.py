# Generated by Django 3.1.3 on 2020-11-13 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_follower'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follower',
        ),
    ]