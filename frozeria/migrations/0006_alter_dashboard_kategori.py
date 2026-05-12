# Generated migration to change kategori foreign key to SET_NULL

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frozeria', '0005_remove_kategori_jumlah_barang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='kategori',
            field=models.ForeignKey(blank=True, db_column='id_kategori', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dashboard_items', to='frozeria.kategori'),
        ),
    ]
