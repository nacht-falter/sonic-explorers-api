# Generated by Django 3.2.4 on 2023-09-17 14:25

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('follows', '0002_auto_20230917_1602'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('owner', 'followed'), name='follows_follow_unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('owner', django.db.models.expressions.F('followed')), _negated=True), name='follows_follow_prevent_self_follow'),
        ),
    ]
