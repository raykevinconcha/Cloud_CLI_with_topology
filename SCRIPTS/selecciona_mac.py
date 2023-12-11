import random

# Leer las direcciones MAC desde el archivo
with open("mac_addresses.txt", "r") as file:
    mac_addresses = file.read().splitlines()

if mac_addresses:
    # Seleccionar una dirección MAC al azar
    mac_seleccionada = random.choice(mac_addresses)
    print("MAC seleccionada:", mac_seleccionada)

    # Eliminar la dirección MAC seleccionada de la lista
    mac_addresses.remove(mac_seleccionada)

    # Actualizar el archivo con las direcciones MAC restantes
    with open("mac_addresses.txt", "w") as file:
        for mac in mac_addresses:
            file.write(mac + "\n")
else:
    print("No hay direcciones MAC disponibles en el archivo.")
