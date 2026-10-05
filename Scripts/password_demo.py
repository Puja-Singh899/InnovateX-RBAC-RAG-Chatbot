from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

users = {
    "alice": "alice123",
    "bob": "bob123",
    "carol": "carol123",
    "david": "david123",
    "eve": "eve123",
    "john": "john123",
}

for username, password in users.items():
    hashed = password_hash.hash(password)

    print(f'"{username}": {{')
    print(f'    "password_hash": "{hashed}",')
    print("}")