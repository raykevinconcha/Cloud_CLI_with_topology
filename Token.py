import json
from openstack_sdk import token_authentication_with_scoped_authorization, password_authentication_with_scoped_authorization


def TokenAdmin(gateway_ip, admin_password, admin_username, admin_domain_name, domain_id, admin_project_name):
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