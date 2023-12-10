import json

import requests
class Instance:

    def __init__(self, id, host, libvirt_name, status, project=None, flavor=None) -> None:
        self.id = id
        self.host = host
        self.libvirt_name = libvirt_name
        self.status = status
        project: Project
        self.project = project
        flavor: Flavor
        self.flavor = flavor

    # status_code = 202
    @classmethod
    def create(cls, auth_endpoint, token, name, flavorRef, imageRef=None, availability_zone=None, network_list=None,
               volume_list=None, compute_version=None):
        url = auth_endpoint + '/servers'
        headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': token,
        }
        if compute_version is not None:
            headers['OpenStack-API-Version'] = 'compute ' + compute_version

        data = \
            {
                'server': {
                    'name': name,
                    'flavorRef': flavorRef
                }
            }

        if imageRef is not None:
            data['server']['imageRef'] = imageRef

        if availability_zone is not None:
            data['server']['availability_zone'] = availability_zone

        if network_list is not None:
            data['server']['networks'] = network_list

        if volume_list is not None:
            data['server']['block_device_mapping'] = volume_list

        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 204
    @classmethod
    def delete(cls, auth_endpoint, token, instance_id):

        url = auth_endpoint + '/servers/{}'.format(instance_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def show(cls, auth_endpoint, token, instance_id):

        url = auth_endpoint + '/servers/{}'.format(instance_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list(cls, auth_endpoint, token, all_tenants=False):

        url = auth_endpoint + '/servers'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        if all_tenants in [1, 't', True, 'true', 'on', 'y', 'yes']:
            params = {all_tenants: True}
        else:
            params = {all_tenants: False}

        r = requests.get(url=url, headers=headers, params=params)
        return r

    # status_code = 200
    @classmethod
    def list_detail(cls, auth_endpoint, token, all_tenants=False, host=None):

        url = auth_endpoint + '/servers/detail'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        if all_tenants in [1, 't', True, 'true', 'on', 'y', 'yes']:
            params = {'all_tenants': True}
        else:
            params = {'all_tenants': False}

        if host is not None:
            params['host'] = host

        r = requests.get(url=url, headers=headers, params=params)

        return r

    # status_code = 200
    @classmethod
    def list_ports(cls, auth_endpoint, token, instance_id):

        url = auth_endpoint + '/servers/{}/os-interface'.format(instance_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list_volumes(cls, auth_endpoint, token, instance_id):

        url = auth_endpoint + '/servers/{}/os-volume_attachments'.format(instance_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    # Compute API version is mandatory
    @classmethod
    def show_console(cls, auth_endpoint, token, instance_id, compute_api_version):

        url = auth_endpoint + '/servers/{}/remote-consoles'.format(instance_id)
        data = \
            {
                "remote_console": {
                    "protocol": "vnc",
                    "type": "novnc"
                }
            }
        headers = \
            {
                'Content-type': 'application/json',
                'X-Auth-Token': token,
                "OpenStack-API-Version": "compute {}".format(compute_api_version)
            }
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 202
    @classmethod
    def action(cls, auth_endpoint, token, instance_id, action):
        url = auth_endpoint + '/servers/{}/action'.format(instance_id)

        if action == 'reboot':
            data = \
                {
                    "reboot": {
                        "type": "HARD"
                    }
                }
        elif action == 'start':
            data = \
                {
                    "os-start": None
                }
        elif action == 'stop':
            data = \
                {
                    "os-stop": None
                }

        headers = \
            {
                'Content-type': 'application/json',
                'X-Auth-Token': token,
            }
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r