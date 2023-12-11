
from openstack_sdk import assign_role_to_user
def asignRole(gateway_ip, admin_token, project_id, user_id, role_id):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    resp = assign_role_to_user(keystone_endpoint, admin_token, project_id, user_id, role_id)
    print(resp.status_code)
    if resp.status_code == 204:
        print('ROL ASIGNADO SUCCESSFULLY')
    else:
        print('ROL NO ASIGNADO')
        return None