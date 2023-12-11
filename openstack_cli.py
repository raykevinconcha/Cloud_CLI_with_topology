from flavor import createFlavor
from instance import createInstance
from network import createNetwork
from ports import createPort
from rol import asignRole
from subnet import createSubnet
from Token import TokenProject,TokenAdmin
def menu():
    global openstackApi
    while True:
        print('''
            1. Ingresar credenciales
            2. Crear red
            3. Crear keypair
            4. Crear o editar grupo de seguridad
            5. Crear VM
            6. Listar VMs
        ''')
        opcion = input('[?] Ingrese su opcion: ')
        print()
        if (opcion=='1'):
            openstackApi.OS_USERNAME = input('[?] Ingrese el usuario: ')
            openstackApi.OS_PASSWORD = input('[?] Ingrese la contraseña: ')
            openstackApi.obtener_token()
        elif (opcion=='2'):
            nombre_red = input('[?] Ingrese el nombre de la red: ')
            nombre_subred = input('[?] Ingrese el nombre de la subred: ')
            cidr = input('[?] Ingrese el CIDR: ')
            segmentation_id = input('[?] Ingrese el segmentation ID: ')

            network_id = openstackApi.crear_red(nombre_red, segmentation_id)
            openstackApi.crear_subred(network_id, nombre_subred, cidr)
        elif (opcion=='3'):
            nombre_llave = input('[?] Ingrese el nombre de la llave: ')
            ruta_llave = input('[?] Ingrese la ruta de la llave: ')
            with open(ruta_llave) as f:
                contenido_llave = f.read()
            openstackApi.crear_keypair(nombre_llave, contenido_llave)
        elif (opcion=='4'):
            print('''
            1. Crear grupo de seguridad
            2. Editar grupo de seguridad
            ''')
            opcion = input('[?] Ingrese su opcion: ')
            print() # imprimir una nueva linea
            if (opcion=='2'):
                lista_sg = openstackApi.obtener_sg()
                # 1. se imprime la lista de security groups
                lista_tabular_sg = [ [sg['id'], sg['name']] for sg in lista_sg] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
                print(tabulate(lista_tabular_sg, headers=['id', 'name']), end="\n\n")
                sg_input = input('[?] Ingrese el nombre del SG a editar: ')
                print() # imprimir una nueva linea
                # 2. se impre las reglas dentro del SG
                sg_id = None
                for sg in lista_sg:
                    if sg['name']==sg_input:
                        sg_id = sg['id'] # a usar en la creacion de la regla
                        lista_tabular_rules =  [ [rule['protocol'], rule['port_range_min'], rule['port_range_max'], rule['remote_ip_prefix']] for rule in sg['security_group_rules']]
                        # para que se impriman los valores por defecto
                        for rule in lista_tabular_rules:
                            if rule[0] == None : rule[0] = 'None'
                            if rule[1] == None : rule[1] = 'None'
                            if rule[2] == None : rule[2] = 'None'
                            if rule[3] == None : rule[3] = '0.0.0.0/0'
                        print(tabulate(lista_tabular_rules, headers=['protocol', 'port_range_min', 'port_range_max', 'remote_ip_prefix']), end="\n\n")
                        break
                # 2. agregar regla de seguridad
                protocolo = input('[?] Ingrese el protocolo (tcp, udp): ')
                puerto = input('[?] Ingrese el puerto: ')
                ip = input('[?] Ingrese el prefijo de IP remoto: ')
                openstackApi.crear_sg_rule(protocolo, puerto, ip, sg_id)
            elif (opcion=='1'):
                nombre = input('[?] Ingrese el nombre del SG a crear: ')
                openstackApi.crear_sg(nombre)
        elif (opcion=='5'):
            # 0. nombre de la vm
            nombre = input('[?] Ingrese el nombre de la vm: ')
            print()
            # 1. seleccionar flavor
            flavors = openstackApi.listar_flavors()
            lista_tabular_flavors = [ [flavor['id'], flavor['name']] for flavor in flavors] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_flavors, headers=['id', 'name']), end="\n\n")
            flavor_id = input('[?] Ingrese el ID del flavor: ')
            print() # imprimir una nueva linea
            # 2. seleccionar imagen
            imagenes = openstackApi.listar_imagenes()
            lista_tabular_imagenes = [ [imagen['id'], imagen['name']] for imagen in imagenes] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_imagenes, headers=['id', 'name']), end="\n\n")
            imagen_id = input('[?] Ingrese el ID de la imagen: ')
            print() # imprimir una nueva linea
            # 3. seleccionar red
            redes = openstackApi.listar_redes()
            lista_tabular_redes = []
            for red in redes:
                id = red['id']
                name = red['name']
                if red['subnets']:
                    subnet_id = red['subnets'][0]
                    subnet_info = openstackApi.obtener_subred(subnet_id)
                    cidr = subnet_info['cidr']
                else:
                    cidr = '-'
                lista_tabular_redes.append([id, name, cidr]) # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_redes, headers=['id', 'name', 'cidr']), end="\n\n")
            red_id = input('[?] Ingrese el ID de la red: ')
            print() # imprimir una nueva linea
            # 4. seleccionar key-pair
            lista_keypair = openstackApi.obtener_keypairs()['keypairs']
            lista_tabular_keypairs = [ [keypair['keypair']['name'], keypair['keypair']['public_key']] for keypair in lista_keypair] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_keypairs, headers=['name', 'public_key']), end="\n\n")
            keypair = input('[?] Ingrese el nombre del keypair: ')
            print() # imprimir una nueva linea
            # 5. seleccionar sg
            lista_sg = openstackApi.obtener_sg()
            lista_tabular_sg = [ [sg['id'], sg['name']] for sg in lista_sg] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_sg, headers=['id', 'name']), end="\n\n")
            sg_id = input('[?] Ingrese el ID del grupo de seguridad: ')
            print() # imprimir una nueva linea
            # 6. se crea la vm
            openstackApi.crear_vm(nombre, flavor_id, imagen_id, red_id, keypair, sg_id)
        elif (opcion=='6'):
            lista_vms = openstackApi.listar_vm()['servers']
            lista_tabular_vm = [ [vm['id'], vm['name']] for vm in lista_vms] # usada para imprimir los datos en una tabla con la libreria 'tabulate'
            print(tabulate(lista_tabular_vm, headers=['id', 'name']), end="\n\n")
            # se obtiene info de una vm en particular
            vm_id = input('[?] Ingrese el ID de la VM para obtener un mayor detalle: ')
            vm_info = openstackApi.obtener_info_vm(vm_id)['server']
            print()
            # 1. nombre
            print(' nombre: '+vm_info['name'])
            # 2. flavor
            flavor_id = vm_info['flavor']['id']
            flavor_info = openstackApi.obtener_info_flavor(flavor_id)['flavor']
            print(' flavor:')
            print('     id: '+vm_info['flavor']['id'])
            print('     nombre: '+flavor_info['name'])
            print('     ram: '+str(flavor_info['ram'])+'mb')
            print('     disk: '+str(flavor_info['disk'])+'gb')
            print('     vcpus: '+str(flavor_info['vcpus']))
            # 3. imagen
            image_id = vm_info['image']['id']
            image_info = openstackApi.obtener_info_imagen(image_id)
            print(' imagen: '+image_info['name'])
            # 4. keyname
            print(' key_name: '+vm_info['key_name'])
            # 5. red, subred e IP
            red = list(vm_info['addresses'].keys())[0]
            direccion_ip = vm_info['addresses'][red][0]['addr']
            print(' red: '+red)
            print(' direccion_ip: '+direccion_ip)
            # 6. grupo de seguridad
            print(' security_group: '+vm_info['security_groups'][0]['name'])