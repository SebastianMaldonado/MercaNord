from django.contrib.auth.models import User
from django.db import models

from BackEnd.App import aplicacion

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.IntegerField(null=False, blank=False, choices=[(categoria.ID, categoria.nombre) for categoria in aplicacion.obtenerCategoria(None, True)])
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Pago(models.Model):
    #('titular', 'tarjeta', 'expira_month', 'expira_year', 'direccion', 'codigo_postal', 'pais')
    titular = models.TextField(blank=True, null=True)
    tarjeta = models.TextField(blank=True, null=True)
    expira_month = models.TextField(blank=True, null=True)
    expira_year = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    codigo_postal = models.TextField(blank=True, null=True)
    pais = models.TextField(blank=True, null=True)
    