# Generated by Django 4.2.7 on 2023-12-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppParts', '0003_alter_parts_image_url_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='parts',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
