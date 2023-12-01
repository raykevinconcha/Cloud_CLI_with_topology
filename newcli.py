import getpass
import pickle
import inquirer
from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
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



usuarios = {
    "admin": {"contraseña": "admin", "rol": "admin", "slices": []},
    "user": {"contraseña": "user", "rol": "usuario_normal", "slices": []}
}

usuarios["admin"]["slices"].append({"Nombre": "Slice AWS Admin", "Arquitectura": "AWS"})
usuarios["user"]["slices"].append({"Nombre": "Slice AWS user", "Arquitectura": "aws"})
usuarios["user"]["slices"].append({"Nombre": "Slice 2", "Arquitectura": "aws"})





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
def crear_slice(usuario, slices_creados, topologias_options):
    arquitectura_options = {
        "1": "Aws",
        "2": "Openstack",
        "3": "Salir"
    }

    arquitectura = print_menu("Selección de Arquitectura", arquitectura_options)
    print(f"Arquitectura seleccionada: {arquitectura}")

    if arquitectura == "3":
        return

    elif arquitectura == "1" or arquitectura == "2":
        while True:
            region_options = {
                "1": "USA",
                "2": "Latinoamerica",
                "3": "Salir"
            }
            region = print_menu("Selección de Region", region_options)
            print(f"Region seleccionada: {region}")

            if region == "3":
                break
            elif region == "1":
                while True:
                    topologia_questions = [
                        inquirer.List('topologia',
                                      message="Selecciona una topología:",
                                      choices=[(topologia, key) for key, topologia in
                                               topologias_options.items()],
                                      )
                    ]
                    topologia_respuesta = inquirer.prompt(topologia_questions)
                    topologia = topologia_respuesta['topologia']
                    print(f"Topología seleccionada: {topologias_options[topologia]}")

                    if topologia == "5":
                        break

                    elif topologia in topologias_options:
                        topo_seleccionada = topologias_options[topologia]

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
                            "Altura": h if h else None
                        }

                        if usuario not in slices_creados:
                            slices_creados[usuario] = []
                        slices_creados[usuario].append(slice_info)

                        print(
                            f"\nSlice creado exitosamente. Detalles del Slice: {slice_info['Nombre']}")
                        cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
                        cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                                     slice_info["Detalle CPUs"]]
                        print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))
                        post_creation_questions = [
                            inquirer.List('post_creation_action',
                                          message="¿Qué acción deseas realizar ahora?",
                                          choices=['Imprimir topología', 'Mostrar JSON', 'Ambos',
                                                   'Volver al menú principal'],
                                          )
                        ]
                        post_creation_action = inquirer.prompt(post_creation_questions)[
                            'post_creation_action']

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

# Función para listar los slices de un usuario
def listar_slices(usuario, slices_creados):
    print("\n=== Listado de Tus Slices ===\n")

    if usuario in slices_creados and slices_creados[usuario]:
        headers = ["ID", "Nombre", "Topología", "CPUs", "RAM (MB)", "Alm. (MB)"]
        table = []

        for idx, slice_info in enumerate(slices_creados[usuario], start=1):
            row = [idx, slice_info['Nombre'], slice_info.get('Topología', 'No especificada'),
                   slice_info.get('Total CPUs', 'N/A'), slice_info.get('Total RAM', 'N/A'),
                   slice_info.get('Total Almacenamiento', 'N/A')]
            table.append(row)

        print(tabulate(table, headers, tablefmt="grid"))

        detalle_opcion = input(
            "\n¿Deseas ver detalles de algún slice? Ingresa el ID o 'salir' para volver al menú: ")
        if detalle_opcion.lower() != 'salir':
            try:
                slice_idx = int(detalle_opcion) - 1
                if 0 <= slice_idx < len(slices_creados[usuario]):
                    selected_slice = slices_creados[usuario][slice_idx]
                    print(f"\nDetalles del Slice: {selected_slice['Nombre']}")
                    if 'Detalle CPUs' in selected_slice:
                        cpu_headers = ["CPU", "RAM (MB)", "Alm. (MB)"]
                        cpu_table = [[cpu['CPU'], cpu['RAM'], cpu['Almacenamiento']] for cpu in
                                     selected_slice["Detalle CPUs"]]
                        print(tabulate(cpu_table, cpu_headers, tablefmt="grid"))
                        imprimir_topologia_opcion = input(
                            "\n¿Deseas imprimir la topología de este slice? (sí/no): ")
                        if imprimir_topologia_opcion.lower() == 'si':
                            if selected_slice['Topología'] == "Malla":
                                crear_topologia_malla_full_mesh(selected_slice['Total CPUs'])
                            elif selected_slice['Topología'] == "Lineal":
                                crear_topologia_lineal(selected_slice['Total CPUs'])
                            elif selected_slice['Topología'] == "Anillo":
                                crear_topologia_anillo(selected_slice['Total CPUs'])
                            elif selected_slice['Topología'] == "Árbol":
                                r = selected_slice.get('Ramificaciones', 2)
                                h = selected_slice.get('Altura', 1)
                                crear_topologia_arbol(r, h)

                    else:
                        print("No hay detalles adicionales disponibles para este slice.")
                else:
                    print("ID de slice no válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número de ID válido.")
    else:
        print("No tienes slices creados.\n")

    input("\nPresiona Enter para volver al menú principal...")


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

    if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
        rol = usuarios[usuario]["rol"]
        print("Bienvenido,", usuario + " (Rol: " + rol + ")!")

        while True:
            if rol == "usuario_normal":
                menu_options = {
                    "1": "Crear slice",
                    "2": "Listar mis slices",
                    "3": "Borrar slice",
                    "4": "Editar Slice",
                    "5": "Salir"
                }
                opcion = print_menu("Menú Principal - Usuario Normal", menu_options)
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

        with open("slices.pkl", "wb") as file:
            pickle.dump(slices_creados, file)
        break
    else:
        print("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
