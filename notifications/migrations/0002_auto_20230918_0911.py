# Generated by Django 3.2.4 on 2023-09-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='is_read',
        ),
        migrations.AddField(
            model_name='notification',
            name='item_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
