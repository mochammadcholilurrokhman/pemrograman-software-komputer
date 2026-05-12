# Generated migration to remove jumlah_barang field from Kategori

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frozeria', '0004_dashboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kategori',
            name='jumlah_barang',
        ),
    ]
