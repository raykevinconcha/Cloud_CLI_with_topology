from openstack_sdk import create_flavor
import  json

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