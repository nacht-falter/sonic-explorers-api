# Generated by Django 3.2.4 on 2023-10-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='review_status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=50),
        ),
    ]
