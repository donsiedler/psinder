# Generated by Django 4.1.1 on 2022-09-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_alter_dog_age_alter_dog_bio_alter_dog_breed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='sex',
            field=models.PositiveSmallIntegerField(choices=[(0, 'suczka'), (1, 'pies')], verbose_name='Płeć'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.PositiveSmallIntegerField(choices=[(0, 'mały'), (1, 'średni'), (2, 'duży'), (3, 'wielki')], verbose_name='Wielkość psa'),
        ),
    ]