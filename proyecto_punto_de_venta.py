import os 
import sys 
from dotenv import load_dotenv
import csv
from datetime import datetime

ARCHIVO_PRODUCTOS = 'productos.csv'

def cargar_productos():
    lista_productos = []
    if not os.path.exists('productos.txt'):
        # Crear archivo con productos iniciales si no existe
        productos_iniciales = [
            ['001', 'Manzana', 2.5, True, 20, 100],
            ['002', 'Pera', 2.0, True, 20, 80],
            ['003', 'Banana', 1.8, True, 20, 120],
            ['004', 'Naranja', 2.2, True, 20, 90],
            ['005', 'Lechuga', 1.5, False, 0, 50],
            ['006', 'Tomate', 2.8, False, 0, 70]
        ]
        with open('productos.txt', 'w') as archivo:
            for p in productos_iniciales:
                archivo.write(f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]}\n")
    if os.path.exists('productos.txt'):
        with open('productos.txt', 'r') as archivo:
            for linea in archivo:
                fila = linea.strip().split(',')
                if len(fila) == 6:
                    codigo = fila[0]
                    nombre = fila[1]
                    precio = float(fila[2])
                    exento_iva = fila[3].lower() == 'true' or fila[3] == 'True'
                    descuento = float(fila[4])
                    stock = float(fila[5])
                    lista_productos.append([codigo, nombre, precio, exento_iva, descuento, stock])
    return lista_productos

def guardar_productos(productos):
    with open('productos.txt', 'w') as f:
        for p in productos:
            f.write(f"{p[0]},{p[1]},{p[2]},{p[3]},{p[4]},{p[5]}\n")

def agregar_producto_al_archivo(producto):
    with open('productos.txt', 'a') as f:
        f.write(f"{producto[0]},{producto[1]},{producto[2]},{producto[3]},{producto[4]},{producto[5]}\n")

productos = cargar_productos()

ARCHIVO_TASA = 'Tasa_de_cambio.txt'


def cargar_tasa_cambio():
    if os.path.exists(ARCHIVO_TASA):
        with open(ARCHIVO_TASA, 'r') as f:
            linea = f.readline().strip()
            if linea:
                # Formato esperado: fecha 1$=valorBS
                partes = linea.split(' ')
                if len(partes) >= 2 and '=' in partes[-1]:
                    valor = partes[-1].replace('BS', '').replace('Bs', '').replace('bs', '')
                    valor = valor.split('=')[-1]
                    if valor.replace('.', '', 1).isdigit():
                        return float(valor)
    return 105  # valor por defecto

def guardar_tasa_cambio(valor):
    fecha = datetime.now().strftime('%d-%m-%Y')
    with open(ARCHIVO_TASA, 'w') as f:
        f.write(f"{fecha} 1$={valor}BS\n")

tasa_cambio = cargar_tasa_cambio()

def es_decimal(texto):
    partes = texto.split('.')
    if len(partes) == 1:
        return partes[0].isdigit()
    elif len(partes) == 2:
        return partes[0].isdigit() and partes[1].isdigit()
    else:
        return False

def es_fruta(nombre):
    frutas = [
        'manzana', 'pera', 'banana', 'naranja', 'mandarina', 'uva', 'fresa', 'mango'
    ]
    return nombre.lower() in frutas

def mostrar_productos():
    print(f'\n--- Lista de Productos ---')
    for p in productos:
        iva = 'Exento' if p[3] else 'Con IVA'
        estado = 'Agotado' if p[5] == 0 else f'{p[5]} kg disponibles'
        print(f'{p[0]} - {p[1]} | $ {p[2]} por kg | {iva} | {p[4]}% desc. | {estado}')

def buscar_producto(codigo):
    i = 0
    while i < len(productos):
        if productos[i][0] == codigo:
            return productos[i]
        i = i + 1
    return None

def calcular_precio(producto, peso):
    precio_dolar = producto[2] * peso
    descuento = producto[4]
    precio_dolar -= precio_dolar * (descuento / 100)
    if not producto[3]:
        precio_dolar *= 1.16 
    precio_bs = precio_dolar * tasa_cambio
    return round(precio_bs, 2)

def eliminar_producto(nombre_producto):
    for i, producto in enumerate(productos):
        if producto[1].lower() == nombre_producto.lower():
            del productos[i]
            print(f'Producto "{nombre_producto}" eliminado.')
            return
    print(f'Producto "{nombre_producto}" no encontrado. No se pudo eliminar.')

def modo_usuario():
    salir = 'no'
    while salir != 'si':
        mostrar_productos()
        codigo = input(f'\nIngrese el código del producto (o \'salir\'): ')
        if codigo == 'salir':
            salir = 'si'
        else:
            producto = buscar_producto(codigo)
            if producto != None:
                if producto[5] == 0:
                    print(f'Producto agotado.')
                else:
                    peso_str = input(f'Ingrese el peso en kg: ')
                    if es_decimal(peso_str):
                        peso = float(peso_str)
                        if peso > producto[5]:
                            print(f'Stock insuficiente. Disponible: {producto[5]} kg.')
                        else:
                            total = calcular_precio(producto, peso)
                            print(f'Usted ha ingresado {peso} kg de {producto[1]} a $ {producto[2]} USD por kg. Total a pagar: Bs {total}')
                            producto[5] = producto[5] - peso   
                    else:
                        print(f'Peso inválido.')
            else:
                print(f'Producto no encontrado.')

def modo_admin():
    load_dotenv()
    CLAVE_SECRETA = os.getenv('SECRET_KEY')

    contra = input(f'Ingrese la contraseña de administrador: ')
    if contra != CLAVE_SECRETA:
        print(f'Contraseña incorrecta.')
        return

    salir = 'no'
    while salir != 'si':
        print(f'\n--- Modo Administrador ---')
        print(f'1. Agregar producto')
        print(f'2. Modificar producto')
        print(f'3. Ver productos')
        print(f'4. Volver al menú principal')
        print(f'5. Cambiar tasa de cambio dólar → Bs')
        print(f'6. Remover Producto')
        opcion = input(f'Opción: ')

        if opcion == '1':
            codigo = input(f'Nuevo código: ')
            if buscar_producto(codigo) == None:
                nombre = input(f'Nombre: ')
                precio_str = input(f'Precio por kg (USD): ')
                if es_decimal(precio_str):
                    precio = float(precio_str)
                    iva = input(f'¿Exento de IVA? (s/n): ')
                    exento = (iva == 's')
                    if es_fruta(nombre):
                        descuento = 20
                        print(f'Producto de fruta detectado: se aplicará un 20% de descuento automáticamente.')
                    else:
                        desc_str = input(f'Descuento %: ')
                        if es_decimal(desc_str):
                            descuento = float(desc_str)
                        else:
                            print(f'Descuento inválido.')
                            descuento = 0
                    stock_str = input(f'Stock disponible (kg): ')  
                    if es_decimal(stock_str):  
                        stock = float(stock_str)
                    else:
                        print(f'Stock inválido, se establecerá en 0.')
                        stock = 0    
                    productos.append([codigo, nombre, precio, exento, descuento, stock])
                    print(f'Producto agregado.')
                else:
                    print(f'Precio inválido.')
            else:
                print(f'Ese código ya existe.')

        elif opcion == '2':  
            codigo = input(f'Código a modificar: ')
            producto = buscar_producto(codigo)
            if producto != None:
                precio_str = input(f'Nuevo precio por kg (USD): ')
                if es_decimal(precio_str):
                    producto[2] = float(precio_str)
                    iva = input(f'¿Exento de IVA? (s/n): ')
                    producto[3] = (iva == 's')
                    if es_fruta(producto[1]):
                        producto[4] = 20
                        print(f'Producto de fruta: se aplica automáticamente un 20% de descuento.')
                    else:
                        desc_str = input(f'Nuevo descuento %: ')
                        if es_decimal(desc_str):
                            producto[4] = float(desc_str)
                        else:
                            print(f'Descuento inválido. Se mantiene el descuento anterior.')
                    stock_str = input(f'Nuevo stock (kg): ')
                    if es_decimal(stock_str):
                        producto[5] = float(stock_str)
                    else:
                        print(f'Stock inválido. Se mantiene el stock anterior.')
                    print(f'Producto modificado.')
                else:
                    print(f'Precio inválido.')
            else:
                print(f'Producto no encontrado.')

        elif opcion == '3':
            mostrar_productos()

        elif opcion == '4':
            salir = 'si'

        elif opcion == '5':
            nueva_tasa = input(f'Nueva tasa de cambio (1 USD = Bs): ')
            if es_decimal(nueva_tasa):
                global tasa_cambio
                tasa_cambio = float(nueva_tasa)
                guardar_tasa_cambio(tasa_cambio)
                print(f'Tasa actualizada: 1 USD = Bs {tasa_cambio}')
            else:
                print(f'Tasa inválida.')
        elif opcion == '6':
            nombre_producto = input(f'Ingrese el nombre del producto que quiere eliminar: ')
            eliminar_producto(nombre_producto)
        else:
            print(f'Opción inválida.')

if __name__ == '__main__':
    salir = 'no'
    while salir != 'si':
        print(f'\n=== Simulador de Balanza ===')
        print(f'1. Usuario')
        print(f'2. Administrador')
        print(f'3. Salir')
        opcion = input(f'Elige una opción: ')
        if opcion == '1':
            modo_usuario()
        elif opcion == '2':
            modo_admin()
        elif opcion == '3':
            salir = 'si'
        else:
            print(f'Opción inválida.')
