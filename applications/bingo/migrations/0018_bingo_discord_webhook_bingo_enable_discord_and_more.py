# Generated by Django 4.1.7 on 2023-09-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0017_alter_bingo_end_date_alter_bingo_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bingo',
            name='discord_webhook',
            field=models.CharField(blank=True, help_text='Webhook URL for your channel.', max_length=256),
        ),
        migrations.AddField(
            model_name='bingo',
            name='enable_discord',
            field=models.BooleanField(default=False, help_text='Should you be notified via discord when something changes?'),
        ),
        migrations.AddField(
            model_name='bingo',
            name='notify_approval',
            field=models.BooleanField(default=False, help_text='Should you be notified when someone approves a tile?'),
        ),
        migrations.AddField(
            model_name='bingo',
            name='notify_completion',
            field=models.BooleanField(default=False, help_text='Should you be notified when someone completes a tile?'),
        ),
        migrations.AddField(
            model_name='bingo',
            name='notify_submission',
            field=models.BooleanField(default=False, help_text='Should you be notified when someone submits a new picture?'),
        ),
    ]
