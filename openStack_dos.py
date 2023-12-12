
import json


from openstack_sdk import create_flavor
from openstack_sdk import create_instance
from openstack_sdk import create_network
from openstack_sdk import create_port
from openstack_sdk import assign_role_to_user
from openstack_sdk import create_subnet
from openstack_sdk import token_authentication_with_scoped_authorization, password_authentication_with_scoped_authorization,create_project






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


def crearProyecto(gateway_ip, token_for_project, domain_id, project_name, project_description):
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


def createSubnet(gateway_ip, token_for_project, network_id, subnet_name, ip_version, cidr):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0'
    resp = create_subnet(neutron_endpoint, token_for_project, network_id, subnet_name, ip_version, cidr)
    if resp.status_code == 201:
        print('SUBNET CREATED SUCCESSFULLY')
        subnet_created = resp.json()
        print(json.dumps(subnet_created))
        return subnet_created
    else:
        print('FAILED SUBNET CREATION')
        return None


def obtenerTokenAdmin(gateway_ip, admin_password, admin_username, admin_domain_name, domain_id, admin_project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'

    resp = password_authentication_with_scoped_authorization(
        keystone_endpoint,
        admin_domain_name,
        admin_username,
        admin_password,
        domain_id,
        admin_project_name
    )

    if resp.status_code == 201:
        admin_token = resp.headers['X-Subject-Token']
        print(f'Token de administrador: {admin_token}')
        return admin_token
    else:
        print('La autenticación del administrador ha fallado')
        return None


def TokenProject(gateway_ip, admin_token, domain_id, project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'

    resp1 = token_authentication_with_scoped_authorization(
        keystone_endpoint,
        admin_token,
        domain_id,
        project_name
    )
    if resp1.status_code == 201:
        token_for_project = resp1.headers['X-Subject-Token']
        print(f'Token del proyecto: {token_for_project}')
        return token_for_project
    else:
        print('FAILED AUTHENTICATION FOR PROJECT ')
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


            token_admin = obtenerTokenAdmin(GATEWAY_IP, ADMIN_PASSWORD, ADMIN_USERNAME, ADMIN_DOMAIN_NAME, DOMAIN_ID,
                                      ADMIN_PROJECT_NAME)

            token = TokenProject(GATEWAY_IP, token_admin, DOMAIN_ID, ADMIN_PROJECT_NAME)

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

                    network_id = create_network(GATEWAY_IP, token, nombre_red)
                    create_subnet(GATEWAY_IP, token, network_id, nombre_subred, IP_VERSION, cidr)

                    pr = crearProyecto(GATEWAY_IP, token, DOMAIN_ID, ADMIN_PROJECT_NAME, project_description)

                    pa = create_port(GATEWAY_IP, token, nombre_red, network_id, pr)

                    pb = create_port(GATEWAY_IP, token, nombre_red, network_id, pr)

                    instance_1_networks = [{"port": pa}]
                    instance_2_networks = [{"port": pb}]


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











