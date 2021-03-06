# Generated by Django 4.0.3 on 2022-03-19 11:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metrics',
            name='Quarter',
        ),
        migrations.RemoveField(
            model_name='metrics',
            name='Year',
        ),
        migrations.AddField(
            model_name='metrics',
            name='Filing_Date',
            field=models.DateField(default=datetime.datetime(2022, 3, 19, 11, 47, 0, 535661, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metrics',
            name='Filing_Type',
            field=models.CharField(choices=[('10k', '10k'), ('10q', '10q'), ('8k', '8k')], default='10k', max_length=3),
        ),
        migrations.AlterField(
            model_name='metrics',
            name='Metric_Type',
            field=models.CharField(choices=[('', ''), ('annual revenue', 'annual revenue'), ('quarterly revenue', 'quarterly revenue'), ('annual liabilities', 'annual liabilities'), ('quarterly liabilities', 'quarterly liabilities'), ('annual profit', 'annual profit'), ('quarterly profit', 'quarterly profit'), ('annual net income', 'annual net income'), ('quarterly net income', 'quarterly net income'), ('annual assets', 'annual assets'), ('quarterly assets', 'quarterly assets')], default='', max_length=21),
        ),
    ]
