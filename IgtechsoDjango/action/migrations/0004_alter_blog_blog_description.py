# Generated by Django 5.0.7 on 2024-08-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0003_alter_blog_blog_date_alter_blog_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_description',
            field=models.TextField(max_length=100),
        ),
    ]
