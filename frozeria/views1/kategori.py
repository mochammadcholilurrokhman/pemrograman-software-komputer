from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from frozeria.models import Kategori
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

def kategori_view(request):
    kategoris = Kategori.objects.all()
    return render(request, 'kategori/index.html', {'kategoris': kategoris})

def tambah_kategori(request):
    if request.method == 'POST':
        nama_kategori = request.POST.get('nama_kategori', '').strip()
        dibuat = request.POST.get('dibuat')
        deskripsi = request.POST.get('deskripsi', '').strip()

        # Validasi nama kategori
        if not nama_kategori:
            messages.error(request, "Nama kategori wajib diisi.")
            return redirect('tambah_kategori')

        # Validasi tanggal dibuat
        if not dibuat:
            messages.error(request, "Tanggal dibuat wajib diisi.")
            return redirect('tambah_kategori')

        # Cek kategori duplikat
        if Kategori.objects.filter(nama_kategori__iexact=nama_kategori).exists():
            messages.error(request, "Kategori dengan nama tersebut sudah ada.")
            return redirect('tambah_kategori')

        # Simpan data
        Kategori.objects.create(
            nama_kategori=nama_kategori,
            dibuat=dibuat,
            deskripsi=deskripsi
        )

        messages.success(request, "Kategori berhasil ditambahkan.")
        return redirect('kategori')

    return render(request, 'kategori/tambah_kategori.html')

def edit_kategori(request, id_kategori):
    kategori = get_object_or_404(Kategori, id_kategori=id_kategori)

    if request.method == 'POST':
        nama_kategori = request.POST.get('nama_kategori', '').strip()
        dibuat = request.POST.get('dibuat')
        deskripsi = request.POST.get('deskripsi', '').strip()

        # Validasi
        if not nama_kategori:
            messages.error(request, "Nama kategori wajib diisi.")
            return redirect('edit_kategori', id_kategori=id_kategori)

        if not dibuat:
            messages.error(request, "Tanggal dibuat wajib diisi.")
            return redirect('edit_kategori', id_kategori=id_kategori)

        # Cek duplicate selain data saat ini
        if Kategori.objects.filter(
            nama_kategori__iexact=nama_kategori
        ).exclude(id_kategori=id_kategori).exists():

            messages.error(request, "Kategori dengan nama tersebut sudah ada.")
            return redirect('edit_kategori', id_kategori=id_kategori)

        # Update data
        kategori.nama_kategori = nama_kategori
        kategori.dibuat = dibuat
        kategori.deskripsi = deskripsi
        kategori.save()

        messages.success(request, "Kategori berhasil diperbarui.")
        return redirect('kategori')

    return render(request, 'kategori/edit_kategori.html', {
        'kategori': kategori
    })

def delete_kategori(request, id_kategori):
    try:
        # Cari kategori berdasarkan ID
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)

        # Hapus kategori
        kategori.delete()

        # Tampilkan pesan sukses
        messages.success(request, f'Kategori {kategori.nama_kategori} berhasil dihapus!')

    except Exception as e:
        # Jika gagal menghapus kategori
        messages.error(request, f'Gagal menghapus Kategori: {e}')

    # Redirect ke halaman daftar user
    return redirect('kategori')

def kategori_datatable(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Column mapping for ordering
        columns = [
            'id_kategori',
            'nama_kategori',
            'jumlah_barang',
            'dibuat',
        ]

        # Get ordering column
        order_column = columns[order_column_idx] if order_column_idx < len(columns) else 'id_kategori'
        if order_direction == 'desc':
            order_column = '-' + order_column

        # Base queryset with related site data
        queryset = Kategori.objects.all()

        # Apply search filter
        if search_value:
            queryset = queryset.filter(
                Q(nama_kategori__icontains=search_value) 
            )

        # Get total count before pagination
        total_records = Kategori.objects.count()
        filtered_records = queryset.count()

        # Apply ordering and pagination
        queryset = queryset.order_by(order_column)[start:start + length]

        # Format data for DataTables
        data = []
        for idx, kategori in enumerate(queryset, start=start + 1):
            # Action buttons
            actions = f'''
                <a href="/frozeria/kategori/edit_kategori/{kategori.id_kategori}/"
                class="btn btn-sm btn-warning me-1">
                    <i class="bi bi-pencil-square"></i> Edit
                </a>
                <a href="#" 
                   class="btn btn-sm btn-danger btn-delete me-1"
                   data-href="/frozeria/kategori/delete_kategori/{kategori.id_kategori}/"
                   data-name="{kategori.nama_kategori}">
                    <i class="bi bi-trash"></i> Hapus
                </a>
            '''

            # Create row data as object for DataTables
            row_data = {
                'nama_kategori': kategori.nama_kategori or '-',
                'jumlah_barang': kategori.get_jumlah_barang(),
                'dibuat': kategori.dibuat.strftime('%H:%M:%S | %d %B %Y') if kategori.dibuat else '-',
                'actions': actions
            }
            data.append(row_data)

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

