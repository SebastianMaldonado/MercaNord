from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import Item
from BackEnd.App import aplicacion

@login_required
def index(request):
    vendedores = aplicacion.obtenerVendedores(f'{request.user}', False)
    items = vendedores[0].productos

    return render(request, 'dashboard/index.html', {
        'items': items,
    })
