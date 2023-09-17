# Generated by Django 4.1.7 on 2023-09-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invocation', '0009_alter_wominvo_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='wominvo',
            name='current_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wominvo',
            name='names',
            field=models.CharField(default='overall', help_text='Name of skills or bosses to track. "overall" for all. Separate by comma', max_length=256),
        ),
    ]