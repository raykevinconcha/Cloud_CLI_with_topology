from tabulate import tabulate
import requests
import json


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
        print('FAILED AUTHENTICATION FOR PROJECT ')
        return None

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
                            2. Crear o editar grupo de seguridad
                            
                        ''')
                opcion = input('[?] Ingrese su opcion: ')
                print()  # imprimir una nueva linea
                if opcion == '1':
                    nombre_red = input('[?] Ingrese el nombre de la red: ')
                    nombre_subred = input('[?] Ingrese el nombre de la subred: ')
                    cidr = input('[?] Ingrese el CIDR: ')



                    network_id = crear_red(token, nombre_red)

                    subred=crear_subred(token, network_id, nombre_subred, cidr)

                    pr = crearProyectonew(token)

                    # pa = create_port(GATEWAY_IP, token, nombre_red, network_id, pr)
                    #
                    # pb = create_port(GATEWAY_IP, token, nombre_red, network_id, pr)
                    #
                    # instance_1_networks = [{"port": pa}]
                    # instance_2_networks = [{"port": pb}]


                    print('''
                                
                                1. Crear VM
                                2. Listar VMs
                            ''')
                    opcion = input('[?] Ingrese su opcion: ')
                    print()  # imprimir una nueva linea
                    if opcion == '3':
                        instance_1_name = input('[?] Ingrese nombre de la VM1: ')
                        instance_2_name = input('[?] Ingrese nombre de la VM2: ')

                        create_instance(GATEWAY_IP, token, instance_1_name, "f66221d0-80d4-4558-9909-838374cf70d7",
                                        '6120912b-1c26-4f8b-b2bb-02225ff5bfea', instance_1_networks)

                        create_instance(GATEWAY_IP, token, instance_2_name, 'f66221d0-80d4-4558-9909-838374cf70d7',
                                        '6120912b-1c26-4f8b-b2bb-02225ff5bfea', instance_2_networks)


menu()









