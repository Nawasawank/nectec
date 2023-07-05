import secrets

jwt_secret_key = secrets.token_hex(12)
print(jwt_secret_key)