import json

import requests
class Port:

    # status_code = 201
    @classmethod
    def create(cls, auth_endpoint, token, name, network_id, project_id):

        url = auth_endpoint + '/ports'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        data = \
            {
                'port': {
                    'name': name,
                    'tenant_id': project_id,
                    'network_id': network_id,
                    'port_security_enabled': 'false'
                }
            }

        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 204
    @classmethod
    def delete(cls, auth_endpoint, token, port_id):

        url = auth_endpoint + '/ports/' + port_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def show(cls, auth_endpoint, token, port_id):

        url = auth_endpoint + '/ports/' + port_id
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list(cls, auth_endpoint, token, network_id=None, instance_id=None):

        url = auth_endpoint + '/ports'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        if network_id is not None:
            r = requests.get(url=url, headers=headers, params={'network_id': network_id})
        elif instance_id is not None:
            r = requests.get(url=url, headers=headers, params={'device_id': instance_id})
        else:
            r = requests.get(url=url, headers=headers)
        return r