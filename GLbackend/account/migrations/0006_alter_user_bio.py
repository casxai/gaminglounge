# Generated by Django 4.2.7 on 2023-12-11 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default='૮ ˶ᵔ ᵕ ᵔ˶ ა', max_length=255),
        ),
    ]