from openstack_sdk import create_port
import json

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
