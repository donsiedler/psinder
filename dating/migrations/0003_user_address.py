# Generated by Django 4.1.1 on 2022-09-18 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='dating.address'),
            preserve_default=False,
        ),
    ]
