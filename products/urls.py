from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.products, name='products'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('update_status/<str:pk>', views.update_status, name='update_status'),
    path('edit_entry/<str:pk>', views.edit_entry, name='edit_entry'),
    path('partial_confirm/<str:pk>', views.partial_confirm, name='partial_confirm'),
    path('search/', views.search, name='search'),
    path('new_sku/', views.new_sku, name='new_sku'),

    path('suppler_orders/<str:pk>', views.suppler_orders, name='suppler_orders'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
