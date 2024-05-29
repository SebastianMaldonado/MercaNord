from django import forms

from .models import Item, Pago
from BackEnd.App import aplicacion

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

        
class NewItemForm(forms.ModelForm):
    
    
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            },
            choices=[(categoria.ID, categoria.nombre) for categoria in aplicacion.obtenerCategoria(None, True)]),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditPaymentForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ('titular', 'tarjeta', 'expira_month', 'expira_year', 'direccion', 'codigo_postal', 'pais')
        widgets = {
            'titular': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'tarjeta': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'expira_month': forms.TextInput(attrs={
                'class': 'py-2 px-2 rounded-xl border'
            }),
            'expira_year': forms.TextInput(attrs={
                'class': 'py-2 px-2 rounded-xl border'
            }),
            'direccion': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'pais': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }
        