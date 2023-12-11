from openstack_sdk import create_subnet
import json


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