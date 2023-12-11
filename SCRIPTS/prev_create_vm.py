import random
import sys

import subprocess

# Función para obtener un número VNC al azar y actualizar el archivo correspondiente
def obtener_port(worker):
    vnc_file = f"vnc_wk{worker}.txt"

    # Leer los números VNC desde el archivo correspondiente al worker
    try:
        with open(vnc_file, "r") as file:
            vnc_numbers = list(map(int, file.read().splitlines()))
    except FileNotFoundError:
        print(f"No se encontró el archivo {vnc_file}. Asegúrate de generarlo primero.")
        return None

    if vnc_numbers:
        # Seleccionar un número VNC al azar
        vnc_seleccionado = random.choice(vnc_numbers)
        print(f"Número VNC seleccionado para Worker {worker}: {vnc_seleccionado}")

        # Eliminar el número VNC seleccionado de la lista
        vnc_numbers.remove(vnc_seleccionado)

        # Actualizar el archivo con los números VNC restantes
        with open(vnc_file, "w") as file:
            for number in vnc_numbers:
                file.write(str(number) + "\n")

        return str(vnc_seleccionado)
    else:
        print(f"No hay números VNC disponibles para Worker {worker}.")
        return None







# Verificar si se proporcionó al menos un argumento (el nombre del script es un argumento)
if len(sys.argv) >= 2:
    parametro_entrada = int(sys.argv[1])  # Convertir a entero

    if parametro_entrada == 1:
        # Ejemplo de uso para Worker 1
        vnc_seleccionado_wk = obtener_port(1)
        VNC = vnc_seleccionado_wk
        if vnc_seleccionado_wk is not None:
            print("Número VNC seleccionado para Worker 1:", vnc_seleccionado_wk)
    elif parametro_entrada == 2:
        # Ejemplo de uso para Worker 2
        vnc_seleccionado_wk = obtener_port(2)
        VNC = vnc_seleccionado_wk
        if vnc_seleccionado_wk is not None:
            print("Número VNC seleccionado para Worker 2:", vnc_seleccionado_wk)
    elif parametro_entrada == 3:
        # Ejemplo de uso para Worker 3
        vnc_seleccionado_wk = obtener_port(3)
        VNC = vnc_seleccionado_wk
        if vnc_seleccionado_wk is not None:
            print("Número VNC seleccionado para Worker 3:", vnc_seleccionado_wk)

    else:
        print("El valor del parámetro de entrada debe ser 1, 2 o 3.")
else:
    print("No se proporcionaron suficientes argumentos. Debes proporcionar al menos un valor como parámetro.")





import random

def obtener_mac_seleccionada():
    archivo = "mac_addresses.txt"

    try:
        # Leer las direcciones MAC desde el archivo
        with open(archivo, "r") as file:
            mac_addresses = file.read().splitlines()

        if mac_addresses:
            # Seleccionar una dirección MAC al azar
            mac_seleccionada = random.choice(mac_addresses)
            print("MAC seleccionada:", mac_seleccionada)

            # Eliminar la dirección MAC seleccionada de la lista
            mac_addresses.remove(mac_seleccionada)

            # Actualizar el archivo con las direcciones MAC restantes
            with open(archivo, "w") as file:
                for mac in mac_addresses:
                    file.write(mac + "\n")

            return mac_seleccionada
        else:
            print(f"No hay direcciones MAC disponibles en el archivo {archivo}.")
            return None
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}. Asegúrate de generarlo primero.")
        return None

# Ejemplo de uso
mac_obtenida = obtener_mac_seleccionada()
if mac_obtenida is not None:
    # Haz algo con la dirección MAC obtenida
    print("Usando MAC:", mac_obtenida)





# Obtener el número VNC del archivo correspondiente al worker
 worker_param = 1  # Reemplaza esto con el parámetro de entrada real


if VNC is not None:
    # Llamar al script en Bash con la MAC y el número VNC seleccionados como argumentos
    bash_script = "create_vm.sh"  # Reemplaza con la ruta real de tu script en Bash

    # Argumentos para el script en Bash
    vm_name = "nombre_vm_generado"
    vlan_id = "id_vlan_generado"
    MAC = mac_obtenida
    VNC_=VNC

    # Concatenar los argumentos para el script en Bash
    args_bash = [bash_script, vm_name, vlan_id, VNC_, MAC]

    # Llamar al script en Bash con los argumentos
    subprocess.run(args_bash)
    print("Script en Bash llamado con la MAC y el número VNC seleccionados como argumentos.")

