# Generated by Django 3.0.3 on 2020-07-12 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default1.jpg', upload_to='profile_pics'),
        ),
    ]
