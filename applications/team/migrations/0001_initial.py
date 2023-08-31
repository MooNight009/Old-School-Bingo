# Generated by Django 3.2.7 on 2023-02-18 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bingo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=64)),
                ('bingo_score', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('bingo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingo.bingo')),
            ],
        ),
    ]
