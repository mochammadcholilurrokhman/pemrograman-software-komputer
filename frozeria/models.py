from django.db import models

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=255)
    dibuat = models.DateTimeField()
    deskripsi = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'kategori'

    def __str__(self):
        return self.nama_kategori
    
    def get_jumlah_barang(self):
        """Menghitung jumlah barang yang terkait dengan kategori ini"""
        return self.dashboard_items.count()
    
class Dashboard(models.Model):
    id_dashboard = models.AutoField(primary_key=True)

    foto_barang = models.ImageField(
        upload_to='foto_barang/',
        blank=True,
        null=True
    )

    nama_barang = models.CharField(max_length=255)

    # Foreign Key ke tabel kategori
    kategori = models.ForeignKey(
        'Kategori',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_kategori',
        related_name='dashboard_items'
    )

    satuan = models.CharField(max_length=100)

    jumlah_stok = models.IntegerField(default=0)

    stok_minimum = models.IntegerField(default=0)

    harga_jual = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    harga_beli = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    berat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    lokasi_simpan = models.CharField(max_length=255)

    deskripsi = models.TextField(blank=True, null=True)

    dibuat = models.DateTimeField(auto_now_add=True)

    diupdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard'

    def __str__(self):
        return self.nama_barang