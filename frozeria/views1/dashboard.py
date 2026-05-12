from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from frozeria.models import Kategori, Dashboard
from django.http import HttpResponse, JsonResponse
from django.db.models import Q


def das_view(request):  # sesuaikan nama view kamu
    kategoris = Kategori.objects.all()
    
    jumlah_barang = Dashboard.objects.count()
    total_kategori = Kategori.objects.count()
    stok_menipis = Dashboard.objects.filter(
        jumlah_stok__gt=0,
        jumlah_stok__lt=20
    ).count()

    stok_habis = Dashboard.objects.filter(jumlah_stok=0).count()
    
    return render(request, 'dashboard/index.html', {
        'kategoris': kategoris,
        'jumlah_barang': jumlah_barang,
        'total_kategori': total_kategori,
        'stok_menipis': stok_menipis,
        'stok_habis': stok_habis,
    })

def detail_dashboard(request, id_dashboard):
    dashboard = get_object_or_404(
        Dashboard,
        id_dashboard=id_dashboard
    )
    
    # Hitung keuntungan per unit
    keuntungan_per_unit = float(dashboard.harga_jual or 0) - float(dashboard.harga_beli or 0)
    
    # Hitung total nilai stok
    total_nilai_stok = float(dashboard.jumlah_stok or 0) * float(dashboard.harga_beli or 0)
    
    return render(request, 'dashboard/detail_dashboard.html', {
        'dashboard': dashboard,
        'keuntungan_per_unit': keuntungan_per_unit,
        'total_nilai_stok': total_nilai_stok
    })

def tambah_dashboard(request):
    kategoris = Kategori.objects.all()

    if request.method == 'POST':
        foto_barang = request.FILES.get('foto_barang')
        nama_barang = request.POST.get('nama_barang', '').strip()
        kategori_id = request.POST.get('kategori')
        satuan = request.POST.get('satuan', '').strip()
        jumlah_stok = request.POST.get('jumlah_stok')
        stok_minimum = request.POST.get('stok_minimum')
        harga_jual = request.POST.get('harga_jual')
        harga_beli = request.POST.get('harga_beli')
        berat = request.POST.get('berat')
        lokasi_simpan = request.POST.get('lokasi_simpan', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()

        # Validasi
        if not nama_barang:
            messages.error(request, "Nama barang wajib diisi.")
            return redirect('tambah_dashboard')

        if not satuan:
            messages.error(request, "Satuan wajib diisi.")
            return redirect('tambah_dashboard')

        # Kategori bersifat opsional
        kategori = None
        if kategori_id:
            try:
                kategori = Kategori.objects.get(id_kategori=kategori_id)
            except Kategori.DoesNotExist:
                messages.error(request, "Kategori tidak ditemukan.")
                return redirect('tambah_dashboard')

        # Simpan data
        Dashboard.objects.create(
            foto_barang=foto_barang,
            nama_barang=nama_barang,
            kategori=kategori,
            satuan=satuan,
            jumlah_stok=jumlah_stok or 0,
            stok_minimum=stok_minimum or 0,
            harga_jual=harga_jual or 0,
            harga_beli=harga_beli or 0,
            berat=berat or 0,
            lokasi_simpan=lokasi_simpan,
            deskripsi=deskripsi
        )

        messages.success(request, "Data barang berhasil ditambahkan.")
        return redirect('dashboard')

    return render(request, 'dashboard/tambah_dashboard.html', {
        'kategoris': kategoris
    })

def edit_dashboard(request, id_dashboard):
    dashboard = get_object_or_404(
        Dashboard,
        id_dashboard=id_dashboard
    )

    kategoris = Kategori.objects.all()

    if request.method == 'POST':

        foto_barang = request.FILES.get('foto_barang')
        nama_barang = request.POST.get('nama_barang', '').strip()
        kategori_id = request.POST.get('kategori')
        satuan = request.POST.get('satuan', '').strip()
        jumlah_stok = request.POST.get('jumlah_stok')
        stok_minimum = request.POST.get('stok_minimum')
        harga_jual = request.POST.get('harga_jual')
        harga_beli = request.POST.get('harga_beli')
        berat = request.POST.get('berat')
        lokasi_simpan = request.POST.get('lokasi_simpan', '').strip()
        deskripsi = request.POST.get('deskripsi', '').strip()
        remove_image = request.POST.get('remove_image', '0')

        # Validasi
        if not nama_barang:
            messages.error(request, "Nama barang wajib diisi.")
            return render(request, 'dashboard/edit_dashboard.html', {
                'dashboard': dashboard,
                'kategoris': kategoris
            })

        if not satuan:
            messages.error(request, "Satuan wajib diisi.")
            return render(request, 'dashboard/edit_dashboard.html', {
                'dashboard': dashboard,
                'kategoris': kategoris
            })

        # Kategori bersifat opsional
        kategori = None
        if kategori_id:
            try:
                kategori = Kategori.objects.get(
                    id_kategori=kategori_id
                )

            except Kategori.DoesNotExist:
                messages.error(request, "Kategori tidak ditemukan.")
                return render(request, 'dashboard/edit_dashboard.html', {
                    'dashboard': dashboard,
                    'kategoris': kategoris
                })

        # Update foto jika upload baru atau hapus jika user klik tombol hapus
        if remove_image == '1':
            # User klik tombol hapus
            if dashboard.foto_barang:
                dashboard.foto_barang.delete()
            dashboard.foto_barang = None
        elif foto_barang:
            # User upload foto baru
            if dashboard.foto_barang:
                dashboard.foto_barang.delete()
            dashboard.foto_barang = foto_barang

        # Update data
        dashboard.nama_barang = nama_barang
        dashboard.kategori = kategori
        dashboard.satuan = satuan
        dashboard.jumlah_stok = jumlah_stok or 0
        dashboard.stok_minimum = stok_minimum or 0
        dashboard.harga_jual = harga_jual or 0
        dashboard.harga_beli = harga_beli or 0
        dashboard.berat = berat or 0
        dashboard.lokasi_simpan = lokasi_simpan
        dashboard.deskripsi = deskripsi

        dashboard.save()

        messages.success(request, "Data barang berhasil diperbarui.")
        return redirect('dashboard')

    return render(request, 'dashboard/edit_dashboard.html', {
        'dashboard': dashboard,
        'kategoris': kategoris
    })

def delete_dashboard(request, id_dashboard):
    dashboard = get_object_or_404(
        Dashboard,
        id_dashboard=id_dashboard
    )
    
    # Hapus gambar jika ada
    if dashboard.foto_barang:
        dashboard.foto_barang.delete()
    
    # Hapus data barang
    dashboard.delete()
    
    messages.success(request, "Data barang berhasil dihapus.")
    return redirect('dashboard')

def das_datatable(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        kategori_id = request.GET.get('kategori_id', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Column mapping
        columns = [
            'id_dashboard',
            'nama_barang',
            'kategori__nama_kategori',
            'jumlah_stok',
            'satuan',
            'harga_jual',
        ]

        # Handle ordering
        if order_column_idx > 0:
            order_column = columns[order_column_idx - 1]
        else:
            order_column = 'id_dashboard'

        if order_direction == 'desc':
            order_column = '-' + order_column

        # Queryset
        queryset = Dashboard.objects.select_related('kategori').all()

        # Filter berdasarkan kategori
        if kategori_id:
            queryset = queryset.filter(kategori_id=kategori_id)

        # Search
        if search_value:
            queryset = queryset.filter(
                Q(nama_barang__icontains=search_value)
            )

        total_records = Dashboard.objects.count()
        filtered_records = queryset.count()

        queryset = queryset.order_by(order_column)[start:start + length]

        data = []

        for idx, dashboard in enumerate(queryset, start=start + 1):

            actions = f'''
                <a href="/frozeria/dashboard/detail_dashboard/{dashboard.id_dashboard}/"
                   class="btn btn-sm btn-info me-1">
                    <i class="bi bi-eye"></i> Detail
                </a>

                <a href="/frozeria/dashboard/edit_dashboard/{dashboard.id_dashboard}/"
                   class="btn btn-sm btn-warning me-1">
                    <i class="bi bi-pencil-square"></i> Edit
                </a>

                <a href="#"
                   class="btn btn-sm btn-danger btn-delete me-1"
                   data-href="/frozeria/dashboard/delete_dashboard/{dashboard.id_dashboard}/"
                   data-name="{dashboard.nama_barang}">
                    <i class="bi bi-trash"></i> Hapus
                </a>
            '''

            row_data = {
                'nama_barang': dashboard.nama_barang or '-',

                'kategori': (
                    dashboard.kategori.nama_kategori
                    if dashboard.kategori else '-'
                ),

                'stok': dashboard.jumlah_stok or 0,

                'satuan': dashboard.satuan or '-',

                'harga_jual': f"Rp {float(dashboard.harga_jual or 0):,.0f}",

                'actions': actions
            }

            data.append(row_data)

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })

    return JsonResponse({
        'error': 'Invalid request'
    }, status=400)

def bantuan_view(request):
    """Render halaman bantuan/panduan penggunaan sistem"""
    return render(request, 'bantuan/index.html')