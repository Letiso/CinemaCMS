# Generated by Django 3.2.9 on 2021-11-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_backgroundimage_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundimage',
            name='color',
            field=models.TextField(default='#f4f6f9', help_text='Если не выбрано'),
        ),
    ]