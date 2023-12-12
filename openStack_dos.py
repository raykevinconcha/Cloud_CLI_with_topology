from tabulate import tabulate
import json

import requests

from openstack_sdk import create_flavor
from openstack_sdk import create_instance
from openstack_sdk import create_network
from openstack_sdk import create_port
from openstack_sdk import assign_role_to_user
from openstack_sdk import create_subnet
from openstack_sdk import token_authentication_with_scoped_authorization,create_project
from openstack_sdk import password_authentication_with_scoped_authorization





def createFlavor(gateway_ip, token_for_project, name, ram, vcpus, disk, flavor_id):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1'
    resp = create_flavor(nova_endpoint, token_for_project, name, ram, vcpus, disk, flavor_id)
    print(resp.status_code)
    if resp.status_code == 200:
        print('INSTANCE CREATED SUCCESSFULLY')
        flavor_created = resp.json()
        print(json.dumps(flavor_created))
        return flavor_created
    else:
        print('FAILED INSTANCE CREATION')
        return None


def createInstance(gateway_ip, token_for_project, instance_name, flavor_id, image_id, networks):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1'
    resp = create_instance(nova_endpoint, token_for_project, instance_name, flavor_id, image_id, networks)
    print(resp.status_code)
    if resp.status_code == 202:
        print('INSTANCE CREATED SUCCESSFULLY')
        instance_created = resp.json()
        print(json.dumps(instance_created))
    else:
        print('FAILED INSTANCE CREATION')
        return None


def createNetwork(gateway_ip, token_for_project, network_name):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0'
    resp3 = create_network(neutron_endpoint, token_for_project, network_name)
    if resp3.status_code == 201:
        print('NETWORK CREATED SUCCESSFULLY')
        network_created = resp3.json()
        print(json.dumps(network_created))
        return network_created
    else:
        print('FAILED NETWORK CREATION')
        return None


def crearProyecto(token_for_project, domain_id, project_name, project_description):
    gateway_ip = '10.20.10.68'
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    resp = create_project(keystone_endpoint, token_for_project, domain_id, project_name, project_description)
    print(resp.status_code)
    if resp.status_code == 201:
        print('PROJECT CREATED SUCCESSFULLY')
        project_created = resp.json()
        print(json.dumps(project_created))
        return project_created
    else:
        print('FAILED PROJECT CREATION')
        return None

def crearProyectonew(token_for_project):
    domain_id = 'default'
    gateway_ip = '10.20.10.68'
    project_name = 'admin'
    project_description = "-"
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    resp = create_project(keystone_endpoint, token_for_project, domain_id, project_name, project_description)


    print('PROJECT CREATED SUCCESSFULLY')
    project_created = resp.json()
    print(json.dumps(project_created))
    return project_created


def createPort(gateway_ip, token_for_project, port_name, network_id, project_id):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0'
    resp = create_port(neutron_endpoint, token_for_project, port_name, network_id, project_id)
    if resp.status_code == 201:
        print('PORT CREATED SUCCESSFULLY')
        port_created = resp.json()
        print(json.dumps(port_created))
        return port_created
    else:
        print('FAILED PORT CREATION')
        return None


def asignRole(gateway_ip, admin_token, project_id, user_id, role_id):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    resp = assign_role_to_user(keystone_endpoint, admin_token, project_id, user_id, role_id)
    print(resp.status_code)
    if resp.status_code == 204:
        print('ROL ASIGNADO SUCCESSFULLY')
    else:
        print('ROL NO ASIGNADO')
        return None





def obtener_token_admin():
    gateway_ip = '10.20.10.68'
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    admin_user_password = 'fa6ca065b77b2e8904897745332a03bd'
    admin_user_username = 'admin'
    admin_user_domain_name = 'Default'
    domain_id = 'default'
    admin_project_name = 'admin'

    resp1 = password_authentication_with_scoped_authorization(keystone_endpoint, admin_user_domain_name,
                                                              admin_user_username, admin_user_password, domain_id,
                                                              admin_project_name)


    print('SUCCESSFUL ADMIN AUTHENTICATION')
    admin_token = resp1.headers['X-Subject-Token']
    return admin_token

def obtener_token_proyecto(admin_token):
    gateway_ip = '10.20.10.68'
    domain_id = 'default'
    project_name = 'admin'

    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    resp = token_authentication_with_scoped_authorization(keystone_endpoint, admin_token, domain_id, project_name)

    if resp.status_code == 201:
        token_for_project = resp.headers['X-Subject-Token']
        print(f'Token del proyecto: {token_for_project}')
        return token_for_project
    else:
        print('FAILED AUTHENTICATION FOR PROJECT ' + project_name)
        return


def listar_flavors(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.COMPUTE_URL + "/flavors"
    return requests.get(url, headers=headers).json()['flavors']


def listar_imagenes(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.GLANCE_URL + "/v2/images"
    return requests.get(url, headers=headers).json()['images']


def listar_redes(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.NETWORK_URL + "/v2.0/networks"
    return requests.get(url, headers=headers).json()['networks']


def crear_red(token_proyecto, nombre_red):
    gateway_ip = '10.20.10.68'
    # ENDPOINTS
    neutron_endpoint = 'http://' + gateway_ip + ':9696/v2.0'

    resp = create_network(neutron_endpoint, token_proyecto, nombre_red)
    if resp.status_code == 201:
        print('NETWORK CREATED SUCCESSFULLY')
        red_creada = resp.json()
        print(json.dumps(red_creada))

        id_red = red_creada["network"]["id"]
        print(f"ID de la red creada: {id_red}")
        return id_red  # Devuelve el ID de la red
    else:
        print('FAILED NETWORK CREATION')
        return None

def crear_subred(token_proyecto, id_red, nombre_subred, cidr):
    gateway_ip = '10.20.10.68'
    # ENDPOINTS
    version_ip = '4'
    neutron_endpoint = 'http://' + gateway_ip + ':9696/v2.0'
    resp = create_subnet(neutron_endpoint, token_proyecto, id_red, nombre_subred, version_ip, cidr)
    if resp.status_code == 201:
        print('SUBNET CREATED SUCCESSFULLY')
        subred_creada = resp.json()
        print(json.dumps(subred_creada))
        return subred_creada
    else:
        print('FAILED SUBNET CREATION')
        return None


def crear_puerto(token_proyecto, nombre_puerto, id_red):
    gateway_ip = '10.20.10.68'
    neutron_endpoint = 'http://' + gateway_ip + ':9696/v2.0'
    id_proyecto = "4c99e29d56344c1088d5c0bca7e9a22c"
    resp = create_port(neutron_endpoint, token_proyecto, nombre_puerto, id_red, id_proyecto)
    if resp.status_code == 201:
        print('PORT CREATED SUCCESSFULLY')
        puerto_creado = resp.json()
        print(json.dumps(puerto_creado))
        # Extraer el ID del puerto
        id_puerto = puerto_creado["port"]["id"]
        print(f"ID del puerto creado: {id_puerto}")
        return id_puerto  # Devuelve el ID del puerto
    else:
        print('FAILED PORT CREATION')
        return None




def crear_instancia(token_proyecto, nombre_instancia, id_flavor, id_imagen, redes):
    gateway_ip = '10.20.10.68'
    nova_endpoint = 'http://' + gateway_ip + ':8774/v2.1'
    resp = create_instance(nova_endpoint, token_proyecto, nombre_instancia, id_flavor, id_imagen, redes)
    if resp.status_code == 202:
        print('INSTANCE CREATED SUCCESSFULLY')
        instancia_creada = resp.json()
        print(json.dumps(instancia_creada))
        return instancia_creada
    else:
        print('FAILED INSTANCE CREATION')
        return None


def listar_flavors(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.COMPUTE_URL + "/flavors"
    return requests.get(url, headers=headers).json()['flavors']


def listar_imagenes(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.GLANCE_URL + "/v2/images"
    return requests.get(url, headers=headers).json()['images']


def listar_redes(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.NETWORK_URL + "/v2.0/networks"
    return requests.get(url, headers=headers).json()['networks']


def obtener_subred(self, subnet_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.NETWORK_URL + '/v2.0/subnets/' + subnet_id
    return requests.get(url, headers=headers).json()['subnet']


def listar_vm(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.COMPUTE_URL + "/servers"
    return requests.get(url, headers=headers).json()


def obtener_info_vm(self, vm_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.COMPUTE_URL + "/servers/" + vm_id
    return requests.get(url, headers=headers).json()


def obtener_sg(self):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.NETWORK_URL + "/v2.0/security-groups"
    response = requests.get(url, headers=headers)
    return response.json()['security_groups']

def obtener_info_flavor(self, flavor_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.COMPUTE_URL + "/flavors/" + flavor_id
    return requests.get(url, headers=headers).json()


def crear_sg_rule(self, protocolo, puerto, ip, sg_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.NETWORK_URL + "/v2.0/security-group-rules"
    data = {
        "security_group_rule": {
            "direction": "ingress",
            "port_range_min": puerto,
            "ethertype": "IPv4",
            "port_range_max": puerto,
            "protocol": protocolo,
            "remote_ip_prefix": ip,
            "security_group_id": sg_id
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())

def obtener_info_imagen(self, image_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': self.TOKEN}
    url = self.GLANCE_URL + "/v2/images/" + image_id
    return requests.get(url, headers=headers).json()

def menu():

    while True:

        GATEWAY_IP = "10.20.10.68"
        DOMAIN_ID = "default"

        ADMIN_PASSWORD = 'fa6ca065b77b2e8904897745332a03bd'
        ADMIN_DOMAIN_NAME = "Default"

        ADMIN_PROJECT_NAME = "proyecto"
        ADMIN_USERNAME = "admin"
        IP_VERSION = "4"

        print('''
            1. Ingresar credenciales
            
        ''')
        opcion = input('[?] Ingrese su opcion: ')
        print()  # imprimir una nueva linea
        if opcion == '1':

            project_description = "-"


            token_admin = obtener_token_admin()
            if token_admin:
                print(f'Token de administrador: {token_admin}')
            else:
                print('Autenticación fallida')

            token = obtener_token_proyecto(token_admin)

            if token:
                print('''
                            1. Crear network y subred
                            2. Editar grupo de seguridad
                            
                        ''')
                opcion = input('[?] Ingrese su opcion: ')
                print()  # imprimir una nueva linea
                if opcion == '1':
                    nombre_red = input('[?] Ingrese el nombre de la red: ')
                    nombre_subred = input('[?] Ingrese el nombre de la subred: ')
                    cidr = input('[?] Ingrese el CIDR: ')



                    network_id = crear_red(token, nombre_red)

                    subred=crear_subred(token, network_id, nombre_subred, cidr)

                    #pr = crearProyectonew(token)


                    pa=crear_puerto(token,nombre_red,network_id)
                    pb=crear_puerto(token,nombre_red,network_id)







                    # instance_1_networks = [{"port": pa}]
                    # instance_2_networks = [{"port": pb}]


                    print('''
                                
                                1. Crear VM
                                2. Listar VMs
                            ''')
                    opcion = input('[?] Ingrese su opcion: ')
                    print()  # imprimir una nueva linea
                    if opcion == '1':
                        instance_1_name = input('[?] Ingrese nombre de la VM1: ')
                        instance_2_name = input('[?] Ingrese nombre de la VM2: ')

                        create_instance(GATEWAY_IP, token, instance_1_name, "f66221d0-80d4-4558-9909-838374cf70d7",
                                        '6120912b-1c26-4f8b-b2bb-02225ff5bfea', instance_1_networks)

                        create_instance(GATEWAY_IP, token, instance_2_name, 'f66221d0-80d4-4558-9909-838374cf70d7',
                                        '6120912b-1c26-4f8b-b2bb-02225ff5bfea', instance_2_networks)
                    if (opcion == '2'):
                        lista_vms = listar_vm()['servers']
                        lista_tabular_vm = [[vm['id'], vm['name']] for vm in
                                            lista_vms]  # usada para imprimir los datos en una tabla con la libreria 'tabulate'
                        print(tabulate(lista_tabular_vm, headers=['id', 'name']), end="\n\n")
                        # se obtiene info de una vm en particular
                        vm_id = input('[?] Ingrese el ID de la VM para obtener un mayor detalle: ')
                        vm_info = obtener_info_vm(vm_id)['server']
                        print()
                        # 1. nombre
                        print(' nombre: ' + vm_info['name'])
                        # 2. flavor
                        flavor_id = vm_info['flavor']['id']
                        flavor_info = obtener_info_flavor(flavor_id)['flavor']
                        print(' flavor:')
                        print('     id: ' + vm_info['flavor']['id'])
                        print('     nombre: ' + flavor_info['name'])
                        print('     ram: ' + str(flavor_info['ram']) + 'mb')
                        print('     disk: ' + str(flavor_info['disk']) + 'gb')
                        print('     vcpus: ' + str(flavor_info['vcpus']))

                    if opcion == '2':
                        redes = listar_redes()
                        lista_tabular_redes = []
                        for red in redes:
                            id = red['id']
                            name = red['name']
                            if red['subnets']:
                                subnet_id = red['subnets'][0]
                                subnet_info = obtener_subred(subnet_id)
                                cidr = subnet_info['cidr']
                            else:
                                cidr = '-'
                            lista_tabular_redes.append([id, name,
                                                        cidr])  # usada para imprimir los datos en una tabla con la libreria 'tabulate'
                        print(tabulate(lista_tabular_redes, headers=['id', 'name', 'cidr']), end="\n\n")
                if opcion == '2':
                    opcion = input('[?] Ingrese su opcion: ')
                    print()  # imprimir una nueva linea
                    if (opcion == '2'):
                        lista_sg = obtener_sg()
                        # 1. se imprime la lista de security groups
                        lista_tabular_sg = [[sg['id'], sg['name']] for sg in
                                            lista_sg]  # usada para imprimir los datos en una tabla con la libreria 'tabulate'
                        print(tabulate(lista_tabular_sg, headers=['id', 'name']), end="\n\n")
                        sg_input = input('[?] Ingrese el nombre del SG a editar: ')
                        print()  # imprimir una nueva linea
                        # 2. se impre las reglas dentro del SG
                        sg_id = None
                        for sg in lista_sg:
                            if sg['name'] == sg_input:
                                sg_id = sg['id']  # a usar en la creacion de la regla
                                lista_tabular_rules = [
                                    [rule['protocol'], rule['port_range_min'], rule['port_range_max'],
                                     rule['remote_ip_prefix']] for rule in sg['security_group_rules']]
                                # para que se impriman los valores por defecto
                                for rule in lista_tabular_rules:
                                    if rule[0] == None: rule[0] = 'None'
                                    if rule[1] == None: rule[1] = 'None'
                                    if rule[2] == None: rule[2] = 'None'
                                    if rule[3] == None: rule[3] = '0.0.0.0/0'
                                print(tabulate(lista_tabular_rules,
                                               headers=['protocol', 'port_range_min', 'port_range_max',
                                                        'remote_ip_prefix']), end="\n\n")
                                break
                        # 2. agregar regla de seguridad
                        protocolo = input('[?] Ingrese el protocolo (tcp, udp): ')
                        puerto = input('[?] Ingrese el puerto: ')
                        ip = input('[?] Ingrese el prefijo de IP remoto: ')
                        crear_sg_rule(protocolo, puerto, ip, sg_id)






menu()









