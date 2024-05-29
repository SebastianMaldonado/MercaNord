from .Usuario import Usuario

class Vendedor (Usuario):
    
    def __init__ (self, ID: int, nombre: str, ventas: int, horario: str, contacto: str, instagram: str, imagen: str):
        super().__init__(ID, nombre, contacto)
        self.imagen = imagen
        self.ventas = ventas
        self.horario = horario
        self.contacto = contacto
        self.instagram = instagram
        self.productos = []
        self.info = f'Disponible durante las horas : {self.horario}\nTeléfono de contacto : {self.contacto}\n{self.instagram}'

    def obtenerID (self):
        return self.ID

    def obtenerInfo (self) -> dict:
        return {'ID': self.ID,
                'nombre': self.nombre,
                'ventas': self.ventas,
                'horario': self.horario,
                'imagen': self.imagen,
                'productos': self.obtenerProductos()}
    
    def obtenerProductos (self) -> list:
        return [producto.obtenerInfo() for producto in self.productos]