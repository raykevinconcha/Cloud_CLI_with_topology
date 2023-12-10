
import json

import requests
class Subnet:

    # status_code = 201
    @classmethod
    def create(cls, auth_endpoint, token, network_id, name, ip_version, cidr):

        url = auth_endpoint + '/subnets'
        data = \
            {
                "subnet": {
                    "network_id": network_id,
                    "name": name,
                    "enable_dhcp": False,
                    "gateway_ip": None,
                    "ip_version": ip_version,
                    "cidr": cidr
                }
            }

        data = data = json.dumps(data)

        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.post(url=url, headers=headers, data=data)
        return r

    # status_code = 204
    @classmethod
    def delete(cls, auth_endpoint, token, subnet_id):

        url = auth_endpoint + '/subnets/' + subnet_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def show(cls, auth_endpoint, token, subnet_id):

        url = auth_endpoint + '/subnets/' + subnet_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list(cls, auth_endpoint, token, network_id=None):

        url = auth_endpoint + '/subnets'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        if network_id is not None:
            r = requests.get(url=url, headers=headers, params={'network_id': network_id})
        else:
            r = requests.get(url=url, headers=headers)
        return r
