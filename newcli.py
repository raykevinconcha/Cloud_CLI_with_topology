import getpass
import pickle
import inquirer
from tabulate import tabulate
import networkx as nx
import mysql.connector
import matplotlib.pyplot as plt



def conectar_a_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydb",
        port="3306"
    )

def guardar_usuarios(usuarios):
    with open("usuarios.pkl", "wb") as file:
        pickle.dump(usuarios, file)

def renombrar_nodos(G):
    nombres_maquinas = {nodo: f"vm{nodo}" for nodo in G.nodes()}
    return nx.relabel_nodes(G, nombres_maquinas)

def crear_topologia_lineal(num_maquinas):
    G = nx.path_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología Lineal")
    plt.show()

def crear_topologia_arbol(r, h):
    G = nx.balanced_tree(r, h)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología de Árbol")
    plt.show()



def crear_topologia_malla_full_mesh(num_maquinas):
    G = nx.complete_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black")
    plt.title("Topología de Malla (Full Mesh)")
    plt.show()


def crear_topologia_anillo(num_maquinas):
    G = nx.cycle_graph(num_maquinas)
    G = renombrar_nodos(G)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    plt.title("Topología de Anillo")
    plt.axis("off")
    plt.show()


def verificar_credenciales(usuario, contraseña):
    conn = conectar_a_bd()
    cursor = conn.cursor()

    try:

        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (usuario, contraseña))


        result = cursor.fetchone()


        cursor.close()
        conn.close()

        if result:
            rol = result[0]
            if rol == 1:
                return "admin"
            else:
                return "rol_desconocido"

        else:
            return None
    except mysql.connector.Error as err:
        print("Error en la base de datos:", err)
        return None





def obtener_datos_usuario():
    preguntas = [
        inquirer.Text('usuario', message="Ingrese su nombre de usuario"),
        inquirer.Password('contraseña', message="Ingrese su contraseña")
    ]
    return inquirer.prompt(preguntas)


def print_menu(title, options):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

    questions = [
        inquirer.List('opcion',
                      message="Selecciona una operación:",
                      choices=[(option, key) for key, option in options.items()],
                      )
    ]
    respuesta = inquirer.prompt(questions)

    print("=" * 50)
    return respuesta['opcion']

# Función para crear un slice
def gestionar_usuarios(usuarios):
    while True:
        print("\n=== Gestión de Usuarios ===\n")
        opciones = {
            "1": "Agregar nuevo usuario",
            "2": "Eliminar usuario",
            "3": "Cambiar contraseña",
            "4": "Salir"
        }
        seleccion = input_menu("Seleccione una opción:", opciones)

        if seleccion == "4":
            break
        elif seleccion == "1":
            nuevo_usuario = input("Ingrese el nombre del nuevo usuario: ")
            nueva_contraseña = input("Ingrese la contraseña del nuevo usuario: ")
            rol = input("Ingrese el rol del nuevo usuario (admin o usuario_normal): ")
            usuarios[nuevo_usuario] = {"contraseña": nueva_contraseña, "rol": rol, "slices": []}
            print(f"Usuario '{nuevo_usuario}' agregado correctamente.")
        elif seleccion == "2":
            usuario_eliminar = input("Ingrese el nombre del usuario a eliminar: ")
            if usuario_eliminar in usuarios:
                del usuarios[usuario_eliminar]
                print(f"Usuario '{usuario_eliminar}' eliminado correctamente.")
            else:
                print("El usuario no existe.")
        elif seleccion == "3":
            usuario_cambiar_contraseña = input("Ingrese el nombre del usuario para cambiar la contraseña: ")
            if usuario_cambiar_contraseña in usuarios:
                nueva_contraseña = input("Ingrese la nueva contraseña: ")
                usuarios[usuario_cambiar_contraseña]["contraseña"] = nueva_contraseña
                print("Contraseña cambiada correctamente.")
            else:
                print("El usuario no existe.")
        else:
            print("Opción no válida.")


# Modifica la función para crear slice
def crear_slice(usuario, slices_creados, topologias_options):
    arquitectura_options = {
        "1": "OpenStack",
        "2": "Linux Cluster",
        "3": "Salir"
    }

    arquitectura = input_menu("Selección de Arquitectura", arquitectura_options)
    print(f"Arquitectura seleccionada: {arquitectura}")

    if arquitectura == "3":
        return

    while True:
        worker_options = {
            "1": "Worker 1",
            "2": "Worker 2",
            "3": "Worker 3",
            "4": "Salir"
        }
        worker = input_menu("Selección de Worker (Región)", worker_options)

        if worker == "4":
            break
        elif worker in ["1", "2", "3"]:
            worker_name = "Worker " + worker
            while True:
                topologia_options = {
                    "1": "Lineal",
                    "2": "Árbol",
                    "3": "Malla",
                    "4": "Anillo",
                    "5": "Salir"
                }
                topologia = input_menu("Selección de Topología", topologia_options)
                print(f"Topología seleccionada: {topologia_options[topologia]}")

                if topologia == "5":
                    break

                elif topologia in topologia_options:
                    topo_seleccionada = topologia_options[topologia]

                    nombre_slice = input("Ingresa un nombre para la slice: ")
                    num_cpus = int(input("Ingresa la cantidad de CPUs: "))

                    # Variables específicas para la topología de árbol
                    r = h = None
                    if topo_seleccionada == "Árbol":
                        r = int(input("Ingrese el número de ramificaciones por nodo: "))
                        h = int(input("Ingrese la altura del árbol: "))

                    total_ram = 0
                    total_almacenamiento = 0
                    cpus_info = []

                    for cpu_num in range(1, num_cpus + 1):
                        print(f"\nDetalles para la CPU {cpu_num}:")
                        ram = int(input("Ingresa la cantidad de RAM en MB para esta CPU: "))
                        almacenamiento = int(
                            input("Ingresa la cantidad de almacenamiento en MB para esta CPU: "))

                        cpus_info.append(
                            {"CPU": cpu_num, "RAM": ram, "Almacenamiento": almacenamiento})
                        total_ram += ram
                        total_almacenamiento += almacenamiento

                    slice_info = {
                        "Nombre": nombre_slice,
                        "Topología": topo_seleccionada,
                        "Total CPUs": num_cpus,
                        "Total RAM": total_ram,
                        "Total Almacenamiento": total_almacenamiento,
                        "Detalle CPUs": cpus_info,
                        "Ramificaciones": r if r else None,
                        "Altura": h if h else None,
                        "Arquitectura": arquitectura,
                        "Worker": worker_name
                    }

                    if usuario not in slices_creados:
                        slices_creados[usuario] = []
                    slices_creados[usuario].append(slice_info)

                    print(f"\nSlice creado exitosamente. Detalles del Slice: {slice_info['Nombre']}")
                    cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
                    cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                                 slice_info["Detalle CPUs"]]
                    print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))

                    post_creation_options = {
                        'Imprimir topología': 'Imprimir topología',
                        'Mostrar JSON': 'Mostrar JSON',
                        'Ambos': 'Ambos',
                        'Volver al menú principal': 'Volver al menú principal'
                    }
                    post_creation_action = input_menu("Acción post-creación", post_creation_options)

                    if post_creation_action == 'Imprimir topología' or post_creation_action == 'Ambos':
                        if slice_info['Topología'] == "Lineal":
                            crear_topologia_lineal(slice_info['Total CPUs'])
                        elif slice_info['Topología'] == "Árbol":
                            r = slice_info.get('Ramificaciones', 2)
                            h = slice_info.get('Altura', 1)
                            crear_topologia_arbol(r, h)
                        elif slice_info['Topología'] == "Malla":
                            crear_topologia_malla_full_mesh(slice_info['Total CPUs'])
                        elif slice_info['Topología'] == "Anillo":
                            crear_topologia_anillo(slice_info['Total CPUs'])
                        else:
                            print("Topología no reconocida.")

                    if post_creation_action in ['Mostrar JSON', 'Ambos']:
                        print(json.dumps(slice_info, indent=4))
                    break
                else:
                    print("Topología no válida. Por favor, selecciona una topología válida.")
        else:
            print("Worker no válido. Por favor, selecciona una región válida.")


# Función para mostrar menú y obtener una selección del usuario
def input_menu(message, options):
    print("\n" + "=" * 50)
    print(f"{message.center(50)}")
    print("=" * 50)

    questions = [
        inquirer.List('opcion',
                      message="Selecciona una opción:",
                      choices=[(option, key) for key, option in options.items()],
                      )
    ]
    respuesta = inquirer.prompt(questions)

    print("=" * 50)
    return respuesta['opcion']



workers = ["Worker 1", "Worker 2", "Worker 3"]

# Función para listar los slices de un usuario
def listar_slices(usuario, slices_creados):
    while True:
        opciones_listado = {
            "1": "Tabla resumen de todas las topologías",
            "2": "JSON con detalle de una topología en particular",
            "3": "Gráfico de topología en particular",
            "4": "Listar imágenes disponibles",
            "5": "Listar recursos disponibles",
            "6": "Volver al menú principal"
        }
        seleccion = input_menu("Opciones de listado de slices", opciones_listado)

        if seleccion == "6":
            break
        elif seleccion == "1":
            mostrar_resumen_topologias(usuario, slices_creados)
        elif seleccion == "2":
            mostrar_detalle_slice(usuario, slices_creados)
        elif seleccion == "3":
            imprimir_topologia_slice(usuario, slices_creados)
        elif seleccion == "4":
            listar_imagenes_disponibles(usuario, slices_creados)
        elif seleccion == "5":
            listar_recursos_disponibles(usuario, slices_creados)
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

def mostrar_resumen_topologias(usuario, slices_creados):
    if usuario in slices_creados and slices_creados[usuario]:
        headers = ["ID", "Nombre", "Topología", "CPUs", "RAM (MB)", "Alm. (MB)"]
        table = []

        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
            row = [idx, slice_info['Nombre'], slice_info.get('Topología', 'No especificada'),
                   slice_info.get('Total CPUs', 'N/A'), slice_info.get('Total RAM', 'N/A'),
                   slice_info.get('Total Almacenamiento', 'N/A')]
            table.append(row)

        print(tabulate(table, headers, tablefmt="grid"))

        detalle_opcion = input("\n¿Deseas ver detalles de algún slice? Ingresa el ID o 'salir' para volver al menú: ")
        if detalle_opcion.lower() != 'salir':
            try:
                slice_idx = int(detalle_opcion) - 1
                if 0 <= slice_idx < len(slices_creados[usuario]):
                    selected_slice = slices_creados[usuario][slice_idx]
                    mostrar_detalle_slice(selected_slice)
                else:
                    print("ID de slice no válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número de ID válido.")
    else:
        print("No tienes slices creados.\n")
def mostrar_detalle_slice(slice_info):
    print(f"\nDetalles del Slice: {slice_info['Nombre']}")
    if 'Detalle CPUs' in slice_info:
        cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
        cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                     slice_info["Detalle CPUs"]]
        print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))
        imprimir_topologia_opcion = input(
            "\n¿Deseas imprimir la topología de este slice? (sí/no): ")
        if imprimir_topologia_opcion.lower() == 'si':
            imprimir_topologia_slice(slice_info)

def imprimir_topologia_slice(slice_info):
    if slice_info['Topología'] == "Malla":
        crear_topologia_malla_full_mesh(slice_info['Total CPUs'])
    elif slice_info['Topología'] == "Lineal":
        crear_topologia_lineal(slice_info['Total CPUs'])
    elif slice_info['Topología'] == "Anillo":
        crear_topologia_anillo(slice_info['Total CPUs'])
    elif slice_info['Topología'] == "Árbol":
        r = slice_info.get('Ramificaciones', 2)
        h = slice_info.get('Altura', 1)
        crear_topologia_arbol(r, h)
    else:
        print("Topología no reconocida.")

def listar_imagenes_disponibles(usuario, slices_creados):
    # Aquí va la lógica para listar las imágenes disponibles
    pass

def listar_recursos_disponibles(usuario, slices_creados):
    # Aquí va la lógica para listar los recursos disponibles
    pass
# Función para borrar un slice
def borrar_slice(usuario, slices_creados):
    print("Selecciona el slice que deseas borrar:")
    if usuario in slices_creados:
        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
            print(f"{idx}. {slice_info['Nombre']}")

        opcion_borrar = input("Ingresa el número del slice a borrar (o 'cancelar' para salir): ")
        if opcion_borrar.lower() == 'cancelar':
            return

        try:
            opcion_borrar = int(opcion_borrar)
            if opcion_borrar >= 1 and opcion_borrar <= len(slices_creados[usuario]):
                slice_borrado = slices_creados[usuario].pop(opcion_borrar - 1)
                print(f"Slice '{slice_borrado['Nombre']}' ha sido borrado correctamente.")
            else:
                print("Número de slice no válido.")
        except ValueError:
            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")
    else:
        print("No tienes slices creados para borrar.")


# Función para editar un slice
def editar_slice(usuario, slices_creados):
    print("\n=== Edición de Slice ===")

    if usuario in slices_creados:
        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
            print(f"{idx}. {slice_info['Nombre']}")

        opcion_editar = input("Ingresa el número de la slice a editar (o 'cancelar' para salir): ")
        if opcion_editar.lower() == 'cancelar':
            return

        try:
            opcion_editar = int(opcion_editar) - 1
            if 0 <= opcion_editar < len(slices_creados[usuario]):
                slice_a_editar = slices_creados[usuario][opcion_editar]

                for cpu in slice_a_editar["Detalle CPUs"]:
                    print(f"\nEditando CPU {cpu['CPU']}:")
                    nuevo_cpu_ram = input(
                        f"  Nueva RAM para CPU {cpu['CPU']} (Actual: {cpu['RAM']} MB, Enter para mantener): ")
                    nuevo_cpu_almacenamiento = input(
                        f"  Nuevo almacenamiento para CPU {cpu['CPU']} (Actual: {cpu['Almacenamiento']} MB, Enter para mantener): ")
                    if nuevo_cpu_ram:
                        cpu['RAM'] = int(nuevo_cpu_ram)
                    if nuevo_cpu_almacenamiento:
                        cpu['Almacenamiento'] = int(nuevo_cpu_almacenamiento)

                print("Slice editado exitosamente.")
            else:
                print("Número de slice no válido.")
        except ValueError:
            print("Opción no válida. Ingresa un número válido o 'cancelar' para salir.")

    else:
        print("No tienes slices creados para editar.")


# Define una función para gestionar usuarios
def gestionar_usuarios(usuarios):
    while True:
        print("\n=== Gestión de Usuarios ===\n")
        opciones = {
            "1": "Agregar nuevo usuario",
            "2": "Eliminar usuario",
            "3": "Cambiar contraseña",
            "4": "Salir"
        }
        seleccion = input_menu("Seleccione una opción:", opciones)

        if seleccion == "4":
            break
        elif seleccion == "1":
            nuevo_usuario = input("Ingrese el nombre del nuevo usuario: ")
            nueva_contraseña = input("Ingrese la contraseña del nuevo usuario: ")
            rol = input("Ingrese el rol del nuevo usuario (admin o usuario_normal): ")
            usuarios[nuevo_usuario] = {"contraseña": nueva_contraseña, "rol": rol, "slices": []}
            print(f"Usuario '{nuevo_usuario}' agregado correctamente.")
        elif seleccion == "2":
            usuario_eliminar = input("Ingrese el nombre del usuario a eliminar: ")
            if usuario_eliminar in usuarios:
                del usuarios[usuario_eliminar]
                print(f"Usuario '{usuario_eliminar}' eliminado correctamente.")
            else:
                print("El usuario no existe.")
        elif seleccion == "3":
            usuario_cambiar_contraseña = input("Ingrese el nombre del usuario para cambiar la contraseña: ")
            if usuario_cambiar_contraseña in usuarios:
                nueva_contraseña = input("Ingrese la nueva contraseña: ")
                usuarios[usuario_cambiar_contraseña]["contraseña"] = nueva_contraseña
                print("Contraseña cambiada correctamente.")
            else:
                print("El usuario no existe.")
        else:
            print("Opción no válida.")


def mostrar_bienvenida():
    print("\n" + "=" * 50)
    print("Bienvenido al Sistema".center(50))
    print("=" * 50)


# Función para obtener los datos del usuario
def obtener_datos_usuario():
    preguntas = [
        inquirer.Text('usuario', message="Ingrese su nombre de usuario"),
        inquirer.Password('contraseña', message="Ingrese su contraseña")
    ]
    return inquirer.prompt(preguntas)

topologias_options = {
    "1": "Lineal",
    "2": "Árbol",
    "3": "Malla",
    "4": "Anillo",
    "5": "Salir"
}

slices_creados = {}

try:
    with open("slices.pkl", "rb") as file:
        slices_creados = pickle.load(file)
except FileNotFoundError:
    slices_creados = {}



def print_menu(title, options):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

    questions = [
        inquirer.List('opcion',
                      message="Selecciona una operación:",
                      choices=[(option, key) for key, option in options.items()],
                      )
    ]
    respuesta = inquirer.prompt(questions)

    print("=" * 50)
    return respuesta['opcion']


while True:
    mostrar_bienvenida()
    datos_usuario = obtener_datos_usuario()
    usuario = datos_usuario['usuario']
    contraseña = datos_usuario['contraseña']
    rol = verificar_credenciales(usuario, contraseña)

    if rol:
        print("Bienvenido,", usuario + " (Rol: " + rol + ")!")

        while True:
            if rol == "admin":
                menu_options = {
                    "1": "Crear slice",
                    "2": "Listar mis slices",
                    "3": "Borrar slice",
                    "4": "Editar Slice",
                    "5": "Gestionar Usuarios",
                    "6": "Salir"
                }
                opcion = print_menu("Menú Principal - Administrador", menu_options)
                print(f"Opción seleccionada: {opcion}")

                if opcion == "6":
                    with open("slices.pkl", "wb") as file:
                        pickle.dump(slices_creados, file)
                    print("¡Hasta luego, " + usuario + "!")
                    break


                elif opcion == "1":
                    crear_slice(usuario, slices_creados, topologias_options)
                elif opcion == "2":
                    listar_slices(usuario, slices_creados)
                elif opcion == "3":
                    borrar_slice(usuario, slices_creados)
                elif opcion == "4":
                    editar_slice(usuario, slices_creados)

                else:
                    print("Opción no válida. Por favor, selecciona una opción válida.")

            else:
                print("Rol no válido.")
                break

        with open("slices.pkl", "wb") as file:
            pickle.dump(slices_creados, file)
        break
    else:
        print("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
