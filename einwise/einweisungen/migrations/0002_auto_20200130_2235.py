# Generated by Django 3.0.2 on 2020-01-30 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('einweisungen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='einweisung',
            options={'verbose_name_plural': 'Einweisungen'},
        ),
        migrations.DeleteModel(
            name='Machine',
        ),
    ]
