# Generated by Django 4.2.7 on 2023-11-03 20:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionInvo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WOMInvo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('XP', 'Experience'), ('KC', 'Bossing'), ('LV', 'Levels')], default='LV', max_length=2)),
                ('amount', models.IntegerField(default=1)),
                ('names', models.CharField(default='overall', help_text='Name of skills or bosses to track. "overall" for all. Separate by comma', max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
