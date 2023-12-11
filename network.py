
from openstack_sdk import create_network
import json

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
