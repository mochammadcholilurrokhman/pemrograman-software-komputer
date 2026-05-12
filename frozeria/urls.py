
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from .views1.dashboard import tambah_dashboard, das_view, das_datatable, edit_dashboard, delete_dashboard, detail_dashboard, bantuan_view
from .views1.kategori import kategori_datatable, kategori_view, tambah_kategori, edit_kategori, delete_kategori

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', lambda request: redirect('/frozeria/dashboard/')),

    # Dashboard
    path ("frozeria/dashboard/", das_view, name='dashboard'),
    path("frozeria/dashboard/detail_dashboard/<int:id_dashboard>/", detail_dashboard, name='detail_dashboard'),
    path("frozeria/dashboard/tambah_dashboard/", tambah_dashboard, name='tambah_dashboard'),
    path("frozeria/dashboard/edit_dashboard/<int:id_dashboard>/", edit_dashboard, name='edit_dashboard'),
    path("frozeria/dashboard/delete_dashboard/<int:id_dashboard>/", delete_dashboard, name='delete_dashboard'),


    # Kategori
    path("frozeria/kategori/", kategori_view, name='kategori'),
    path("frozeria/kategori/tambah_kategori/", tambah_kategori, name='tambah_kategori'),
    path("frozeria/kategori/edit_kategori/<int:id_kategori>/", edit_kategori, name='edit_kategori'),
    path("frozeria/kategori/delete_kategori/<int:id_kategori>/", delete_kategori, name='delete_kategori'),

    path('frozeria/dashboard/das_datatable/', das_datatable, name='das_datatable'),
    path('frozeria/kategori/kategori_datatable/', kategori_datatable, name='kategori_datatable'),

    # Bantuan
    path('frozeria/bantuan/', bantuan_view, name='bantuan'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
