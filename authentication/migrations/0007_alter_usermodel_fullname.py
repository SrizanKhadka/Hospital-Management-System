# Generated by Django 5.0.6 on 2024-07-02 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_usermodel_jobtitle_usermodel_joined_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='fullName',
            field=models.CharField(max_length=200),
        ),
    ]
