# Generated by Django 4.2.7 on 2023-12-11 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ('-modified_at',)},
        ),
    ]
