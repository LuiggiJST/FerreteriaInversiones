
# SISTEMA DE GESTIÓN DOCUMENTAL
# Ferretería Inversiones Córdoba Pintado IRL
# El sistema registra únicamente compras realizadas a proveedores.
import json
import math
import os
import getpass
from datetime import datetime

# ==========================================
# GESTIÓN DE USUARIOS Y AUTENTICACIÓN
# ==========================================
# Cuentas individuales para cada encargado con su respectiva contraseña y rol
usuarios_sistema = {
    "carlos_prov": {
        "contrasena": "clave123",
        "rol": "proveedores",
        "nombre_completo": "Carlos Proveedores"
    },
    "ana_prov": {
        "contrasena": "segura456",
        "rol": "proveedores",
        "nombre_completo": "Ana Logística"
    },
    "admin_cordoba": {
        "contrasena": "admin2026",
        "rol": "administrador",
        "nombre_completo": "Administrador General"
    }
}


# Devuelve la fecha y hora actual para mostrarla en pantalla.
def fecha_hora_actual():
    return datetime.now().strftime("%d/%m/%Y  %H:%M:%S")


# Pide la contraseña y muestra un asterisco (*) por cada letra que se escribe.
def leer_contrasena_oculta(mensaje):
    try:
        import msvcrt  # sirve en Windows (VS Code)
    except ImportError:
        return getpass.getpass(mensaje)  # en otros sistemas no se ve nada

    print(mensaje, end="", flush=True)
    clave = ""
    while True:
        tecla = msvcrt.getwch()  # lee una tecla sin mostrarla
        if tecla == "\r":  # Enter: termina de escribir
            print()
            return clave
        elif tecla == "\x03":  # Ctrl + C: cancela el programa
            raise KeyboardInterrupt
        elif tecla == "\b":  # Borrar: quita la última letra
            if clave:
                clave = clave[:-1]
                print("\b \b", end="", flush=True)
        else:  # cualquier otra tecla: se guarda y se muestra *
            clave += tecla
            print("*", end="", flush=True)


def iniciar_sesion():
    print("=============================================")
    print("       SISTEMA DE ACCESO RESTRINGIDO")
    print("     INVERSIONES CÓRDOBA PINTADO IRL")
    print("=============================================")
    print("Fecha y hora:", fecha_hora_actual())

    intentos = 3
    while intentos > 0:
        usuario_ingresado = input("Ingrese su usuario: ").strip()
        mostrar = leer_opcion("¿Desea mostrar la contraseña al escribirla? (si/no): ",
                              ("si", "sí", "no"))
        if mostrar == "no":
            contrasena_ingresada = leer_contrasena_oculta("Ingrese su contraseña: ").strip()
        else:
            contrasena_ingresada = input("Ingrese su contraseña: ").strip()

        # Verificamos si el usuario existe y la contraseña coincide
        if usuario_ingresado in usuarios_sistema and usuarios_sistema[usuario_ingresado]["contrasena"] == contrasena_ingresada:
            datos_usuario = usuarios_sistema[usuario_ingresado]

            # Verificamos que tenga rol de proveedores o administrador
            if datos_usuario["rol"] == "proveedores" or datos_usuario["rol"] == "administrador":
                print(f"\n¡Bienvenido/a, {datos_usuario['nombre_completo']}! Acceso concedido.")
                print("Ingreso:", fecha_hora_actual())
                return True
            else:
                print("\n[Acceso Denegado] Su cuenta no pertenece al personal autorizado de proveedores.\n")
                return False
        else:
            intentos -= 1
            print(f"Usuario o contraseña incorrectos. Te quedan {intentos} intentos.\n")

    print("Acceso bloqueado por seguridad. Demasiados intentos fallidos.")
    return False


# Listas para guardar los datos de cada documento.
# Los datos que están en la misma posición son del mismo documento.
limite = 100
codigos = [None] * limite
proveedores = [None] * limite
rucs = [None] * limite
tipos = [None] * limite
numeros = [None] * limite
fechas = [None] * limite
productos = [None] * limite
cantidades = [None] * limite
precios = [None] * limite
montos = [0.0] * limite
estados = [None] * limite
cantidad_documentos = 0

# Juntamos las listas para poder mover todos los datos de un documento juntos.
listas = [codigos, proveedores, rucs, tipos, numeros,
          fechas, productos, cantidades, precios, montos, estados]


# Menú principal
# Cada número lleva a una parte del sistema.
def menu():
    while True:
        print("\n=============================================")
        print("       SISTEMA DE GESTIÓN DOCUMENTAL")
        print("     INVERSIONES CÓRDOBA PINTADO IRL")
        print("=============================================")
        print("Fecha y hora:", fecha_hora_actual())
        print("1. Registrar documento")
        print("2. Validar documento")
        print("3. Buscar documento")
        print("4. Ordenar documentos")
        print("5. Mostrar documentos")
        print("6. Guardar documentos en archivo")
        print("7. Salir")
        opcion = leer_opcion("Elija una opción: ", ("1", "2", "3", "4", "5", "6", "7"))

        if opcion == "1":
            registrar_documento()
        elif opcion == "2":
            validar_documento()
        elif opcion == "3":
            buscar_documento()
        elif opcion == "4":
            ordenar_documentos()
        elif opcion == "5":
            mostrar_documentos()
        elif opcion == "6":
            guardar_documentos()
        elif opcion == "7":
            salir()
            break

        input("\nPresione Enter para volver al menú.")


# Funciones sencillas para pedir y revisar datos.
def leer_opcion(mensaje, opciones):
    while True:
        dato = input(mensaje).strip().lower()
        if dato in opciones:
            return dato
        print("Escriba una de estas opciones:", ", ".join(opciones))


def leer_texto(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Este dato no puede quedar vacío.")


def leer_ruc(mensaje, obligatorio=True):
    while True:
        dato = input(mensaje).strip()
        if not dato and not obligatorio:
            return "No registrado"
        if len(dato) == 11 and dato.isdigit():
            return dato
        print("Escriba un RUC de 11 números.")


def leer_fecha():
    while True:
        dato = input("Fecha (día/mes/año): ").strip()
        try:
            fecha = datetime.strptime(dato, "%d/%m/%Y")
            return fecha.strftime("%d/%m/%Y")
        except ValueError:
            print("Escriba una fecha válida, por ejemplo 17/10/2026.")


def leer_cantidad():
    while True:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad > 0:
                return cantidad
        except ValueError:
            pass
        print("Ingrese una cantidad entera mayor que cero.")


def leer_precio():
    while True:
        try:
            precio = float(input("Precio por unidad (S/): ").replace(",", "."))
            if math.isfinite(precio) and precio > 0:
                return precio
        except ValueError:
            pass
        print("Ingrese un precio mayor que cero.")


def leer_tipo():
    opciones = ("factura", "boleta", "otro")
    mensaje = "Tipo de comprobante (factura, boleta u otro): "
    return leer_opcion(mensaje, opciones)


# Mostramos juntos todos los datos de un comprobante.
def mostrar_documento(posicion):
    print("\n---------------------------------------------")
    print("Código:", codigos[posicion])
    print("Proveedor:", proveedores[posicion])
    print("RUC:", rucs[posicion])
    print("Comprobante:", tipos[posicion], numeros[posicion])
    print("Fecha:", fechas[posicion])

    for lugar in range(len(productos[posicion])):
        importe = cantidades[posicion][lugar] * precios[posicion][lugar]
        print(f"Producto: {productos[posicion][lugar]}")
        print(f"  {cantidades[posicion][lugar]} x S/ {precios[posicion][lugar]:.2f} = S/ {importe:.2f}")

    print(f"Monto total: S/ {montos[posicion]:.2f}")
    print("Estado:", estados[posicion])


# 1. Registrar documento
# Aquí se registran las facturas y comprobantes de compra.
def registrar_documento():
    global cantidad_documentos

    if cantidad_documentos == limite:
        print("Ya se llegó al límite de documentos.")
        return

    nombre = leer_texto("Nombre del proveedor: ")
    ruc = leer_ruc("RUC del proveedor: ")
    tipo = leer_tipo()
    numero = leer_texto("Número del comprobante: ").upper()

    # Revisamos que el comprobante no se haya ingresado antes.
    for posicion in range(cantidad_documentos):
        repetido = (rucs[posicion] == ruc
                    and tipos[posicion] == tipo
                    and numeros[posicion] == numero)
        if repetido:
            print("Ese comprobante ya está registrado.")
            return

    fecha = leer_fecha()
    lista_productos = []
    lista_cantidades = []
    lista_precios = []
    total = 0

    # Se pueden ingresar varios productos en el mismo comprobante.
    while True:
        producto = leer_texto("Nombre del producto: ")
        cantidad = leer_cantidad()
        precio = leer_precio()
        importe = round(cantidad * precio, 2)
        if not math.isfinite(total + importe):
            print("El monto es demasiado grande; vuelva a ingresar este producto.")
            continue

        lista_productos.append(producto)
        lista_cantidades.append(cantidad)
        lista_precios.append(precio)
        total = round(total + importe, 2)

        agregar = leer_opcion("¿Desea agregar otro producto? (si/no): ", ("si", "sí", "no"))
        if agregar == "no":
            break

    posicion = cantidad_documentos
    codigos[posicion] = f"DOC-{cantidad_documentos + 1:03d}"
    proveedores[posicion] = nombre
    rucs[posicion] = ruc
    tipos[posicion] = tipo
    numeros[posicion] = numero
    fechas[posicion] = fecha
    productos[posicion] = lista_productos
    cantidades[posicion] = lista_cantidades
    precios[posicion] = lista_precios
    montos[posicion] = total
    estados[posicion] = "Pendiente de revisión"
    cantidad_documentos += 1

    print("\nDocumento registrado correctamente.")
    mostrar_documento(posicion)


# 2. Validar documento
# Revisamos los datos ingresados y los comparamos con el comprobante físico.
def validar_documento():
    if cantidad_documentos == 0:
        print("Todavía no hay documentos registrados.")
        return

    codigo = input("Escriba el código del documento (ejemplo DOC-001): ").strip().upper()
    posicion = -1
    for lugar in range(cantidad_documentos):
        if codigos[lugar] == codigo:
            posicion = lugar
            break

    if posicion == -1:
        print("No se encontró ese código.")
        return

    mostrar_documento(posicion)

    # Volvemos a sumar los productos para comprobar el monto.
    total_calculado = 0
    datos_correctos = bool(proveedores[posicion] and tipos[posicion]
                           and numeros[posicion] and fechas[posicion])
    datos_correctos = datos_correctos and len(rucs[posicion]) == 11 and rucs[posicion].isdigit()
    for lugar in range(len(productos[posicion])):
        if cantidades[posicion][lugar] <= 0 or precios[posicion][lugar] <= 0:
            datos_correctos = False
        total_calculado += cantidades[posicion][lugar] * precios[posicion][lugar]

    if round(total_calculado, 2) != round(montos[posicion], 2):
        datos_correctos = False

    if not datos_correctos:
        estados[posicion] = "Por corregir"
        print("Revise las cantidades, precios y monto total.")
        return

    respuesta = leer_opcion("¿Los datos coinciden con el comprobante físico? (si/no): ",
                            ("si", "sí", "no"))
    if respuesta == "no":
        estados[posicion] = "Por corregir"
        print("El documento quedó marcado para corregir.")
    else:
        estados[posicion] = "Validado"
        print("Documento validado.")


# 3. Buscar documento
# Se puede buscar por proveedor, fecha o tipo de comprobante.
def buscar_documento():
    if cantidad_documentos == 0:
        print("Todavía no hay documentos registrados.")
        return

    print("\n1. Por proveedor")
    print("2. Por fecha")
    print("3. Por tipo de comprobante")
    opcion = leer_opcion("Elija cómo desea buscar: ", ("1", "2", "3"))

    if opcion == "1":
        dato = leer_texto("Escriba el nombre o una parte del nombre: ").lower()
    elif opcion == "2":
        dato = leer_fecha()
    else:
        dato = leer_texto("Escriba el tipo de comprobante: ").lower()

    encontrados = 0
    for posicion in range(cantidad_documentos):
        if opcion == "1":
            coincide = dato in proveedores[posicion].lower()
        elif opcion == "2":
            coincide = fechas[posicion] == dato
        else:
            coincide = tipos[posicion] == dato

        if coincide:
            mostrar_documento(posicion)
            encontrados += 1

    if encontrados == 0:
        print("No se encontraron documentos.")
    else:
        print("\nDocumentos encontrados:", encontrados)


# 4. Ordenar documentos
# El método burbuja compara documentos vecinos y los cambia de lugar si hace falta.
def ordenar_documentos():
    if cantidad_documentos == 0:
        print("Todavía no hay documentos para ordenar.")
        return

    print("\n1. Por fecha")
    print("2. Por proveedor")
    print("3. Por tipo de comprobante")
    opcion = leer_opcion("Elija cómo desea ordenar: ", ("1", "2", "3"))

    for vuelta in range(cantidad_documentos - 1):
        for posicion in range(cantidad_documentos - 1 - vuelta):
            siguiente = posicion + 1
            if opcion == "1":
                actual = datetime.strptime(fechas[posicion], "%d/%m/%Y")
                despues = datetime.strptime(fechas[siguiente], "%d/%m/%Y")
            elif opcion == "2":
                actual = proveedores[posicion].lower()
                despues = proveedores[siguiente].lower()
            else:
                actual = tipos[posicion]
                despues = tipos[siguiente]

            if actual > despues:
                for lista in listas:
                    guardado = lista[posicion]
                    lista[posicion] = lista[siguiente]
                    lista[siguiente] = guardado

    print("Documentos ordenados.")
    mostrar_documentos()


# 5. Mostrar documentos
# Se presentan todos los comprobantes registrados y sus montos.
def mostrar_documentos():
    if cantidad_documentos == 0:
        print("Todavía no hay documentos registrados.")
        return

    total_compras = 0
    for posicion in range(cantidad_documentos):
        mostrar_documento(posicion)
        total_compras += montos[posicion]

    print("\nDocumentos registrados:", cantidad_documentos)
    print(f"Total de compras registradas: S/ {total_compras:.2f}")


# 6. Guardar documentos
# Se crea un archivo digital con los datos registrados.
def guardar_documentos():
    documentos = []
    for posicion in range(cantidad_documentos):
        documento = {
            "codigo": codigos[posicion],
            "proveedor": proveedores[posicion],
            "ruc": rucs[posicion],
            "tipo": tipos[posicion],
            "numero": numeros[posicion],
            "fecha": fechas[posicion],
            "productos": productos[posicion],
            "cantidades": cantidades[posicion],
            "precios": precios[posicion],
            "monto_total": montos[posicion],
            "estado": estados[posicion]
        }
        documentos.append(documento)

    # El archivo se guarda en la misma carpeta donde está este programa.
    carpeta = os.path.dirname(os.path.abspath(__file__))
    nombre_archivo = os.path.join(carpeta, "documentos_ferreteria.json")
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(documentos, archivo, ensure_ascii=False, indent=4)
    except OSError as error:
        print("No se pudo guardar el archivo:", error)
        return

    print("Se guardaron", len(documentos), "documento(s) en:")
    print(nombre_archivo)


# 7. Salir
def salir():
    print("Programa finalizado.")


# Al ejecutar la celda, primero se solicita el inicio de sesión y luego se inicia el menú.
if __name__ == "__main__":
    if iniciar_sesion():
        menu()



