# Generated by Django 4.2.7 on 2023-12-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anasjamlaoui', '0004_alter_announcement_anc_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='anc_date',
            field=models.DateTimeField(),
        ),
    ]
