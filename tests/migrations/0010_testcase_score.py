# Generated by Django 3.0.8 on 2020-08-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_auto_20200813_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='score',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
    ]
