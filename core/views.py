from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm, LoginForm, SignupSellerForm
from django.core.files.storage import FileSystemStorage

import os

from BackEnd.App import aplicacion
from django.contrib.auth import views as auth_views


def index(request):
    print(request.user)
    print(aplicacion.obtenerUsuario(request.user))
    
    items = aplicacion.obtenerArticulos(None, True)[:6]
    categories = aplicacion.obtenerCategoria(None, True)
    vendedores = aplicacion.obtenerVendedores(None, True)[0:3]

    return render(request, 'core/index.html', {
        'vendedores': vendedores,
        'categories': categories,
        'items': items,
    })
    
def inventario (request):
    print(aplicacion.obtenerUsuario(f'{request.user}'))
    
    # Validar que el usuario sea un Vendedor
    # Si no lo es redirigir a formulario
    if (aplicacion.usuarioVendedor(f'{request.user}')):
        print('Vendedor')
        return redirect('/dashboard/')
    
    # Si lo es redirigir al dashboard    
    return redirect('/vendedor/')

def carrito (request):
    return redirect('/carrito/')

def vendedor (request):
    if request.method == 'POST':
        form = SignupSellerForm(request.POST, request.FILES)
        
        if form.is_valid():
            horario = form.cleaned_data['horario']
            contacto = form.cleaned_data['contacto']
            instagram = form.cleaned_data['instagram']

            aplicacion.registrarVendedor(horario, contacto, instagram, f'001SR.png')
            
            return redirect('/dashboard/')
            
    else:
        form = SignupSellerForm()
        
    return render(request, 'core/vendedor.html', {
        'form': form
    })


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password']
            
            print(aplicacion.obtenerUsuario(f'{request.user}'))
            
            auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm)

            return redirect('/base/')
    else:
        
        form = LoginForm()

    return render(request, 'core/login.html', {
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            print('Iniciando Registro de Usuario')
            aplicacion.registrarUsuario(username, email, password1, password2)

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })