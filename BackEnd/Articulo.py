from .Vendedor import Vendedor
from .Categoria import Categoria

class Articulo:

    def __init__ (self, ID: int, nombre: str, precio: int, descripcion: str, ventas: int, imagen: str, vendedor: Vendedor, categoria: Categoria):
        self.ID = ID
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.ventas = ventas
        self.imagen = imagen
        self.vendedor = vendedor
        self.categoria = categoria

    def obtenerInfo (self) -> dict:
        return {'ID': self.ID,
                'nombre': self.nombre,
                'precio': self.precio,
                'ventas': self.ventas,
                'imagen': self.imagen,
                'vendedor': self.vendedor.obtenerID(),
                'categoria': self.categoria.obtenerID()}