import random

def generar_mac(prefix="00:16:3e"):
    mac_address = [int(x, 16) for x in prefix.split(':')] + [
                   random.randint(0x00, 0xff),
                   random.randint(0x00, 0xff),
                   random.randint(0x00, 0xff)]

    return ':'.join(map(lambda x: "%02x" % x, mac_address))

def mac_no_repetida(mac_list, prefix="00:16:3e"):
    nueva_mac = generar_mac(prefix)
    while nueva_mac in mac_list:
        nueva_mac = generar_mac(prefix)
    mac_list.append(nueva_mac)
    return nueva_mac

# Lista para almacenar las MAC generadas
macs_generadas = []

# Generar 5 MACs no repetidas con un prefijo personalizado
for _ in range(5):
    nueva_mac = mac_no_repetida(macs_generadas, "00:1a:2b")
    print("MAC generada:", nueva_mac)
    macs_generadas.append(nueva_mac)

# Guardar las MACs en un archivo
with open("../mac_addresses.txt", "w") as file:
    for mac in macs_generadas:
        file.write(mac + "\n")

print("Direcciones MAC guardadas en mac_addresses.txt")

