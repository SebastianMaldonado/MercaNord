from .Categoria import Categoria
from .Articulo import Articulo
from .Vendedor import Vendedor
from .Usuario import Usuario
import os

class app:

    def __init__ (self):
        self.dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.articulos = []
        self.categorias = []
        self.vendedores = []
        self.usuario = None
    
    def obtenerUsuario (self, nombre) -> bool:
        direccion_usuarios = f"{self.dir}/staticfiles/Datos/Usuarios.csv"
        
        if (self.usuario is not None):
            return True
        
        archivo = open(direccion_usuarios)
        for info_usuario in archivo:
            try:
                nombre_usuario, correo, password_usuario = info_usuario.split(';')
                if (f'{nombre}' == nombre_usuario):
                    self.usuario = Usuario(0, nombre, correo)
                    return True
            except:
                continue
            
        self.usuario = None
        return False
    
    def obtenerVendedor (self, nombre, password) -> bool:
        direccion_usuarios = f"{self.dir}/staticfiles/Datos/Vendedores.csv"
        
        archivo = open(direccion_usuarios)
        for info_usuario in archivo:
            datos = info_usuario.split(';')
            nombre_usuario = datos[0]
            password_usuario = datos[7]
            if (nombre == nombre_usuario and password == password_usuario):
                self.usuario = Usuario(nombre)
                return True
            
        self.usuario = None
        return False
    
    def usuarioVendedor (self, nombre) -> bool:
        print(nombre)
        resultado = self.obtenerVendedores(nombre, False)
        print(resultado)
        if (len(resultado) == 0):
            return False
        
        return True
    
    def registrarUsuario (self, nombre, correo, password, repetir_password) -> bool:
        direccion_usuario = f"{self.dir}/staticfiles/Datos/Usuarios.csv"
                
        archivo = open(direccion_usuario, 'a')
        registro = f'\n{nombre};{correo};{password}'
        archivo.write(registro)
        print('Usuario Registrado')
        return True
    
    def registrarVendedor (self, horario, contacto, instagram, imagen) -> bool:
        direccion_vendedores = f"{self.dir}/staticfiles/Datos/Vendedores.csv"
        
        archivo = open(direccion_vendedores, 'a')
        ID = len(self.vendedores)
        registro = f'\n{ID};{self.usuario.nombre};0;{horario};{contacto};{instagram};{imagen};password'
        archivo.write(registro)
        
        vendedor = Vendedor(ID, self.usuario.nombre, 0, horario, contacto, instagram, imagen)
        self.vendedores.append(vendedor)
        print('Vendedor Registrado')
        return True
    
    def cargarProductos (self) -> None:
        direccion_productos = f"{self.dir}/staticfiles/Datos/Productos"
        direccion_imagenes_prod = 'media\item_images'
        direccion_imagenes_vend = 'media\page_images'
        direccion_vendedores = f"{self.dir}/staticfiles/Datos/Vendedores.csv"

        #Cargar Vendedores
        vendedor_defecto = Vendedor(0, 'Sin Vendedor registrado', 0, '00:00 - 23:59', '3000000000', '@defecto','vendedor_por_defecto')
        self.vendedores.append(vendedor_defecto)
        
        archivo = open(direccion_vendedores)
        for articulos in archivo:
            datos = articulos.split(';')
            ID = int(datos[0])
            nombre = datos[1]
            ventas = int(datos[2])
            horario = datos[3]
            contacto = datos[4]
            instagram = datos[5]
            imagen = f'{direccion_imagenes_vend}\{datos[6]}'.replace('\n', '')

            vendedor = Vendedor(ID, nombre, ventas, horario, contacto, instagram, imagen)
            self.vendedores.append(vendedor)

        #Cargar Categorias y Productos
        categorias = os.listdir(direccion_productos)
        for categoria in categorias:
            ID = len(self.categorias)
            nombre = categoria.split('.')[0]

            nueva_categoria = Categoria(ID, nombre)
            self.categorias.append(nueva_categoria)

            archivo = open(f"{direccion_productos}\{categoria}", "r")
            for articulos in archivo:
                datos = articulos.split(';')
                ID = int(datos[0])
                nombre = datos[1]
                precio = int(datos[2])
                descripcion = datos[3]
                ventas = int(datos[4])
                imagen = f'{direccion_imagenes_prod}\{datos[5]}'
                print(int(datos[6]))
                vendedor = self.obtenerVendedores(int(datos[6]), False)[0]
                categoria = nueva_categoria

                producto = Articulo(ID, nombre, precio, descripcion, ventas, imagen, vendedor, nueva_categoria)
                self.articulos.append(producto)
                vendedor.productos.append(producto)
                nueva_categoria.ingresarProducto(producto)
                nueva_categoria.generarImagen()
    
    def obtenerVendedores (self, criterio, orden: bool) -> list:
        if (type(criterio) == str): #Nombre
            vendedores = [vendedor for vendedor in self.vendedores if vendedor.nombre == criterio]
        elif (type(criterio) == int):   #ID
            vendedores = [vendedor for vendedor in self.vendedores if vendedor.ID == criterio]
        else:   #None
            vendedores = self.vendedores

        if (orden):
            n = len(vendedores)
            for i in range(n-1):       # <-- bucle padre
                for j in range(n-1-i): # <-- bucle hijo
                    if vendedores[j].ventas > vendedores[j+1].ventas:
                        vendedores[j], vendedores[j+1] = vendedores[j+1], vendedores[j]
            vendedores = vendedores[::-1]
            print([vendedor.nombre for vendedor in vendedores])

        return vendedores

    def obtenerCategoria (self, criterio, orden: bool) -> list:
        if (type(criterio) == int):   #ID
            categorias = [categoria for categoria in self.categorias if categoria.ID == criterio]
        else:   #None
            categorias = self.categorias

        if (orden):
            n = len(categorias)
            for i in range(n-1):       # <-- bucle padre
                for j in range(n-1-i): # <-- bucle hijo
                    if categorias[j].cant > categorias[j+1].cant:
                        categorias[j], categorias[j+1] = categorias[j+1], categorias[j]
            categorias = categorias[::-1]

        return categorias

    def obtenerArticulos (self, criterio, orden: bool) -> list:
        if (type(criterio) == str): #Nombre
            articulos = [articulo for articulo in self.articulos if criterio in articulo.nombre]
        elif (type(criterio) == int):   #ID
            articulos = [articulo for articulo in self.articulos if articulo.ID == criterio]
        else:   #None
            articulos = self.articulos

        if (orden):
            n = len(articulos)
            for i in range(n-1):       # <-- bucle padre
                for j in range(n-1-i): # <-- bucle hijo
                    if articulos[j].ventas > articulos[j+1].ventas:
                        articulos[j], articulos[j+1] = articulos[j+1], articulos[j]
            articulos = articulos[::-1]

        return articulos
    
    def comprarArticulos (self) -> None:
        return None
    
    def agregarArticulo (self, nombre:str, ID_categoria:int, descripcion:str, precio:int, imagen:str) -> int:       
        categoria = self.obtenerCategoria(ID_categoria, False)[0]
        ID = (len(categoria.productos) + 1)*1000 + (ID_categoria + 1)
        precio = int(precio)
        
        direccion_categoria = ""
        if (ID_categoria == 0):
            direccion_categoria = f"{self.dir}\Datos\Productos\Alimentos Dulces.csv" 
        elif (ID_categoria == 1):
            direccion_categoria = f"{self.dir}\Datos\Productos\Detalles.csv" 
        elif (ID_categoria == 2):
            direccion_categoria = f"{self.dir}\Datos\Productos\Mecatos.csv"
        elif (ID_categoria == 3):
            direccion_categoria = f"{self.dir}\Datos\Productos\Miscelania.csv"
        elif (ID_categoria == 4):
            direccion_categoria = f"{self.dir}\Datos\Productos\\Utencilios.csv"
        else:
            return
                
        archivo = open(direccion_categoria, 'a')
        vendedor = self.obtenerVendedores(self.usuario.nombre, False)[0]
        print(type(self.usuario.nombre))
        print(vendedor.obtenerInfo())
        
        registro = f'{ID};{nombre};{precio};{descripcion};0;{imagen};{vendedor.ID}\n'
        archivo.write(registro)
        
        articulo = Articulo(ID, nombre, precio, 0, 0, imagen, vendedor, categoria)
        self.articulos.append(articulo)
        vendedor.productos.append(articulo)
        categoria.productos.append(articulo)
        
        print('Articulo Agregado')
        return ID

    def modificarArticulo (self, item: Articulo, nombre: str, descripcion: str, precio: int, imagen: str):
        item.nombre = nombre
        item.descripcion = descripcion
        item.precio = precio
        item.imagen = imagen
        
        self.eliminarArticulo(item, item.categoria)
        self.agregarArticulo(nombre, item.categoria.ID, descripcion, precio, imagen)
        
    def eliminarArticulo (self, item: Articulo, categoria: Categoria) -> None:
        nuevo_registro = ""
        ID_categoria = categoria.ID
        
        # Eliminar en Memoria
        self.articulos.remove(item)
        item.vendedor.productos.remove(item)
        categoria.productos.remove(item)
        
        # Eliminar en Archivos
        direccion_categoria = ""
        if (ID_categoria == 0):
            direccion_categoria = f"{self.dir}/staticfiles/Datos/Productos\Alimentos Dulces.csv" 
        elif (ID_categoria == 1):
            direccion_categoria = f"{self.dir}/staticfiles/Datos/Productos\Detalles.csv" 
        elif (ID_categoria == 2):
            direccion_categoria = f"{self.dir}/staticfiles/Datos/Productos\Mecatos.csv"
        elif (ID_categoria == 3):
            direccion_categoria = f"{self.dir}/staticfiles/Datos/Productos\Miscelania.csv"
        elif (ID_categoria == 4):
            direccion_categoria = f"{self.dir}/staticfiles/Datos/Productos\\Utencilios.csv"
        else:
            return
        
        archivo = open(direccion_categoria, 'r')
        for linea in archivo:
            if (item.ID != int(linea.split(';')[0])):
                nuevo_registro += linea
            
        archivo.close()
        
        archivo = open(direccion_categoria, 'w')
        archivo.write(nuevo_registro)
        archivo.close()
    
aplicacion = app()
aplicacion.cargarProductos()
