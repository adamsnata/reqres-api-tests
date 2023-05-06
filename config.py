from dataclasses import dataclass

base_url = 'https://reqres.in/api'

post_users_body = {
            "name": "Ivan",
            "job": "Chemist"
        }


put_users_body = {
    "name": "morpheus",
    "job": "zion resident"
}


post_register_body = {

    "email": "eve.holt@reqres.in",
    "password": "pistol"
    }

post_login_body_invalid = {

        "email": "peter@klaven"
    }


post_login_body = {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka"
    }


@dataclass
class Hosts:
    def __init__(self, env):
        self.demoqa = {
            'local': 'localhost:5555',
            'prod': 'https://demowebshop.tricentis.com',
        }[env]
        self.reqres = {
            'local': 'localhost:5555',
            'prod': 'https://reqres.in/api',
        }[env]
