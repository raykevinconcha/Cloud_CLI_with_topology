from openstack_sdk import create_instance
import json


def createInstance(gateway_ip, token_for_project, instance_name,flavor_id , image_id, networks):
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