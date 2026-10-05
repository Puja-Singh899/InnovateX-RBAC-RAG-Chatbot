from jose import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

token = input("Paste your JWT locally: ").strip()

payload = jwt.get_unverified_claims(token)

print("\nOriginal payload:")
print(payload)

payload["role"] = "executive"

print("\nTampered payload:")
print(payload)

tampered_token = jwt.encode(
    payload,
    "wrong-secret",
    algorithm=ALGORITHM
)

print("\nTampered token:")
print(tampered_token)