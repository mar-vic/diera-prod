# Generated by Django 3.1.4 on 2021-03-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_extensions', '0002_featuredextension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredextension',
            name='featured',
            field=models.BooleanField(default=False, help_text='Check, if the event is supposed to be featured on the homepage', verbose_name='FEATURED'),
        ),
    ]
