import json

import requests
class Network:

    # status_code = 201
    @classmethod
    def create(cls, auth_endpoint, token, name, network_type=None, segmentation_id=None):

        url = auth_endpoint + '/networks'
        data = \
            {
                "network": {
                    "name": name,
                    "port_security_enabled": "false",
                }
            }

        if network_type is not None:
            data['network']["provider:network_type"] = network_type

        if segmentation_id is not None:
            data["network"]["provider:segment"] = segmentation_id

        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 204
    @classmethod
    def delete(cls, auth_endpoint, token, network_id):

        url = auth_endpoint + '/networks/' + network_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def show(cls, auth_endpoint, token, network_id):

        url = auth_endpoint + '/networks/' + network_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list(cls, auth_endpoint, token):

        url = auth_endpoint + '/networks'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r
