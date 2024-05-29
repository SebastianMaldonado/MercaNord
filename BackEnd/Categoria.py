from random import randint

class Categoria:

    def __init__ (self, ID: int, nombre: str):
        self.ID = ID
        self.nombre = nombre
        self.productos = []
        self.cant = 0
        self.generarImagen()

    def generarImagen (self):
        if len(self.productos) == 0:
            self.imagen = '/media/page_images/categoria_por_defecto.png'
            return
        
        num_aleatorio = randint(0, len(self.productos) - 1)
        articulo_aleatorio = self.productos[num_aleatorio]
        self.imagen = articulo_aleatorio.imagen
    
    def ingresarProducto (self, producto):
        self.productos.append(producto)
        self.cant += 1

    def obtenerID (self):
        return self.ID

    def obtenerInfo (self) -> dict:
        return {'ID': self.ID,
                'nombre': self.nombre,
                'imagen': self.imagen,
                'productos': self.obtenerProductos()}

    def obtenerProductos (self) -> list:
        return [producto.obtenerInfo() for producto in self.productos]