# Generated by Django 3.0.2 on 2021-07-17 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('einweisungen', '0006_auto_20200218_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='einweisung',
            options={'permissions': [('view_all', 'View all einweisungen')], 'verbose_name_plural': 'Einweisungen'},
        ),
    ]
