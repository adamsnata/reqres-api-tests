from voluptuous import Schema
new_user_schema = Schema(
    {
        "name": str,
        "job": str,
        "id": str,
        "createdAt": str
    }
)


user_register_schema = Schema(
    {
        "id": int,
        "token": str
    }
)