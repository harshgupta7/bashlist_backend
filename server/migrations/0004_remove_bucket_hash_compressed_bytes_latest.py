# Generated by Django 2.0 on 2018-06-28 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_bucket_hash_compressed_bytes_latest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='hash_compressed_bytes_latest',
        ),
    ]