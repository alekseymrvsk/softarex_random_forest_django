# Generated by Django 4.0.6 on 2022-07-13 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_userprofile_bio_remove_userprofile_facebook_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='n_predict',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]
