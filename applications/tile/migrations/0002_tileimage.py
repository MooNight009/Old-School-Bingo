# Generated by Django 4.2.7 on 2023-11-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('background', models.CharField(choices=[('', 'Transparent')], default='', max_length=64)),
                ('style', models.CharField(choices=[('', 'Wiki')], default='', max_length=64)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]
