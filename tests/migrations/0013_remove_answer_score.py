# Generated by Django 3.0.8 on 2020-08-17 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0012_answer_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='score',
        ),
    ]
