# Generated by Django 4.1.1 on 2022-09-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0010_meeting_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='target_dog_sex',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'kobieta'), (1, 'mężczyzna')], null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='target_user_gender',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'kobieta'), (1, 'mężczyzna')], null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(0, 'kobieta'), (1, 'mężczyzna')], verbose_name='Płeć'),
        ),
    ]