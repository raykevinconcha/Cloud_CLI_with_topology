import json

import requests


class User:

    # status_code = 201
    @classmethod
    def password_authentication_with_unscoped_authorization(cls, auth_endpoint, user_domain_id, username, password):

        url = auth_endpoint + '/auth/tokens'

        data = \
            {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "name": username,
                                "domain": {
                                    "id": user_domain_id
                                },
                                "password": password
                            }
                        }
                    }
                }
            }

        r = requests.post(url=url, data=json.dumps(data))

        return r

    # status_code = 201
    @classmethod
    def token_authentication_with_unscoped_authorization(cls, auth_endpoint, token):

        url = auth_endpoint + '/auth/tokens'

        data = \
            {
                "auth": {
                    "identity": {
                        "methods": [
                            "token"
                        ],
                        "token": {
                            "id": token
                        }
                    }
                }
            }

        r = requests.post(url=url, data=json.dumps(data))

        return r

    # status_code = 201
    @classmethod
    def password_authentication_with_scoped_authorization(cls, auth_endpoint, user_domain_name, username, password,
                                                          project_domain_id, project_name):

        url = auth_endpoint + '/auth/tokens'

        data = \
            {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "name": username,
                                "domain": {
                                    "name": user_domain_name
                                },
                                "password": password
                            }
                        }
                    },
                    "scope": {
                        "project": {
                            "domain": {
                                "id": project_domain_id
                            },
                            "name": project_name
                        }
                    }
                }
            }

        r = requests.post(url=url, data=json.dumps(data))

        return r

    # status_code = 201
    @classmethod
    def token_authentication_with_scoped_authorization(cls, auth_endpoint, token, project_domain_id, project_id):

        url = auth_endpoint + '/auth/tokens'

        data = \
            {
                "auth": {
                    "identity": {
                        "methods": [
                            "token"
                        ],
                        "token": {
                            "id": token
                        }
                    },
                    "scope": {
                        "project": {
                            "domain": {
                                "id": project_domain_id
                            },
                            "name": project_id
                        }
                    }
                }
            }
        r = requests.post(url=url, data=json.dumps(data))

        return r

    # status_code = 204
    @classmethod
    def revoke_token(cls, auth_endpoint, x_auth_token, user_token):
        url = auth_endpoint + '/auth/tokens'

        headers = {
            'X-Auth-Token': x_auth_token,
            'X-Subject-Token': user_token
        }

        r = requests.delete(url=url, headers=headers)

        return r

    # status_code = 201
    @classmethod
    def create(cls, auth_endpoint, token, username, password, description, email, domain_id):

        url = auth_endpoint + '/users'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        data = \
            {
                "user": {
                    "domain_id": domain_id,
                    "enabled": True,
                    "name": username,
                    "password": password,
                    "description": description,
                    "email": email
                }
            }

        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 204
    @classmethod
    def delete(cls, auth_endpoint, token, user_id):

        url = auth_endpoint + '/users/{}'.format(user_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.delete(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def show(cls, auth_endpoint, token, user_id):

        url = auth_endpoint + '/users/{}'.format(user_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 200
    @classmethod
    def list(cls, auth_endpoint, token):

        url = auth_endpoint + '/users'
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.get(url=url, headers=headers)
        return r

    # status_code = 204



    # status_code = 200
    @classmethod
    def update(cls, auth_endpoint, token, user_id, email, new_password=None):

        url = auth_endpoint + '/users/{}'.format(user_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        if new_password == None:
            data = \
                {
                    "user": {
                        "email": email,
                    }
                }
        else:
            data = \
                {
                    "user": {
                        "email": email,
                        "password": new_password,
                    }
                }

        r = requests.patch(url=url, headers=headers, data=json.dumps(data))
        return r

    # status_code = 200
    @classmethod
    def list_project_of_user(cls, auth_endpoint, token, user_id):

        url = auth_endpoint + '/users/{}/projects'.format(user_id)
        headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

        r = requests.get(url=url, headers=headers)
        return r

