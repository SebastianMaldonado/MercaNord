from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    
    path('<int:pk>/add_carrito/', views.agregarCarrito, name='add'),
    path('<int:pk>/rem_carrito/', views.eliminarCarrito, name='del'),
    path('comprar/', views.comprarCarrito, name='com'),
    path('carrito/', views.carrito, name='carrito'),
    
    path('pago/', views.pago, name='pago')
]
