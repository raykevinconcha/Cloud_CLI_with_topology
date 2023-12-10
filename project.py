import json

import requests

class Project:

    def __init__(self, id, name, domain_id, description) -> None:
        self.id = id
        self.name = name
        self.domain_id = domain_id
        self.description = description

    # status_code = 201
    @classmethod
    def create(cls, auth_endpoint, token, domain_id, project_name, project_description):

        url = auth_endpoint + '/projects'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        data = \
            {
                "project": {
                    "name": project_name,
                    "description": project_description,
                    "domain_id": domain_id
                }
            }

        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 201

    # status_code = 200, 400 if empty project_name or project_description
    @classmethod
    def update(cls, auth_endpoint, token, project_id, project_name=None, project_description=None):

        url = auth_endpoint + '/projects/{}'.format(project_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}  # Scoped token

        data = {'project': {}}

        if project_name is not None:
            data['project']['name'] = project_name
        if project_description is not None:
            data['project']['description'] = project_description

        r = requests.patch(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 204
    @classmethod
    def assign_role_to_user_on_project(cls, auth_endpoint, token, project_id, user_id, role_id):

        url = auth_endpoint + '/projects/{}/users/{}/roles/{}'.format(project_id, user_id, role_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.put(url=url, headers=headers)
        return r

    # status_code = 204
    @classmethod
    def unassign_role_to_user_on_project(cls, auth_endpoint, token, project_id, user_id, role_id):

        url = auth_endpoint + '/projects/{}/users/{}/roles/{}'.format(project_id, user_id, role_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list_roles_of_user_on_project(cls, auth_endpoint, token, project_id, user_id):

        url = auth_endpoint + '/projects/{}/users/{}/roles'.format(project_id, user_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.get(url=url, headers=headers)
        return r