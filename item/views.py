from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage

import os

from .forms import NewItemForm, EditItemForm, EditPaymentForm
from BackEnd.Articulo import Articulo

from BackEnd.App import aplicacion

def items(request):
    query = request.GET.get('query', '')
    category_id = int(request.GET.get('category', 0))
    items = aplicacion.obtenerArticulos(None, False)
    categories = aplicacion.obtenerCategoria(None, False)
    vendedores = aplicacion.obtenerVendedores(None, False)

    if category_id:
        items = [producto for producto in aplicacion.obtenerArticulos(None, False) if producto.categoria.ID == category_id]

    if query:
        items = aplicacion.obtenerArticulos(query, False)
        print(query)
        print([producto.categoria.ID for producto in aplicacion.obtenerArticulos(None, False) if producto.nombre == query])

    return render(request, 'item/items.html', {
        'vendedores': vendedores,
        'categories': categories,
        'items': items,
        'query': query,
        'category_id': int(category_id)
    })

def detail(request, pk):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    item = aplicacion.obtenerArticulos(pk, True)[0]
    related_items = [producto for producto in aplicacion.obtenerCategoria(item.categoria.nombre, True)[0].productos if producto != item][0:3]
    usuario = aplicacion.usuario
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'usuario': usuario
    })
    
@login_required
def new(request):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            nombre = form.cleaned_data['name']
            categoria = form.cleaned_data['category']
            descripcion = form.cleaned_data['description']
            precio = form.cleaned_data['price']
            imagen = form.cleaned_data['image']
            
            # Guardar Imagen
            direccion_programa = os.path.dirname(os.path.dirname(__file__))
            direccion_imagenes = f'{direccion_programa}/static/media/item_images'
            FileSystemStorage(location=direccion_imagenes).save(f'{nombre}.png', imagen)
            
            ID_articulo = aplicacion.agregarArticulo(nombre, categoria, descripcion, precio, f'{nombre}.png')

            return redirect('item:detail', pk=ID_articulo)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    #item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item = aplicacion.obtenerArticulos(pk, True)[0]

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES)

        if form.is_valid():
            nombre = form.cleaned_data['name']
            descripcion = form.cleaned_data['description']
            precio = form.cleaned_data['price']
            imagen = form.cleaned_data['image']
            
            # Guardar Imagen
            direccion_programa = os.path.dirname(os.path.dirname(__file__))
            direccion_imagenes = f'{direccion_programa}/static/media/item_images'
            FileSystemStorage(location=direccion_imagenes).save(f'{nombre}.png', imagen)
            
            aplicacion.modificarArticulo(item, nombre, descripcion, precio, f'{nombre}.png')

            return redirect('item:detail', pk=pk)
    else:
        form = EditItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    item = aplicacion.obtenerArticulos(pk, True)[0]
    
    aplicacion.eliminarArticulo(item, item.categoria)

    return redirect('dashboard:index')

@login_required
def carrito (request):
    print('Mostrando el carrito')
    
    return render(request, 'item/carrito.html', {
        'items': aplicacion.usuario.carrito,
    })

@login_required
def agregarCarrito (request, pk):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    item = aplicacion.obtenerArticulos(pk, True)[0]
    
    aplicacion.usuario.carrito.append(item)
    
    return redirect('item:carrito')

@login_required
def eliminarCarrito (request, pk):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    item = aplicacion.obtenerArticulos(pk, True)[0]
    
    try:
        aplicacion.usuario.carrito.remove(item)
    except:
        print("Objeto no existe en el Carrito")
        
    return redirect('item:carrito')

@login_required
def comprarCarrito (request):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    return redirect('item:pago')
    
@login_required
def pago (request):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    saldo = sum([articulo.precio for articulo in aplicacion.usuario.carrito])
    form = EditPaymentForm()
    
    if request.method == 'POST':
        aplicacion.usuario.carrito = []
        return redirect('core:index')
    
    return render(request, 'item/pago.html', {
        'items': aplicacion.usuario.carrito,
        'saldo': saldo,
        'form': form
    })
    