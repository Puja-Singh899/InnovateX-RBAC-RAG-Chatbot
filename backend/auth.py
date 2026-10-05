import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt

load_dotenv()
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            return None

        return {
            "username": username,
            "role": role
        }

    except Exception:
        return None


USERS = {
    "alice": {
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$xh2ZusCBNoVe19y8+feCyg$ovMdz9a2+gvRbrMcmdw+xpJagH/qguvHMsgJwcjN6Fs",
        "role": "finance"
    },
    "bob": {
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$7q8SVTxSP8R7Rfsqd2C91Q$zlCZn4IW4IqaCNxMywxdGL3P3uoAPBIwuAtA6H+74zQ",
        "role": "marketing"
    },
    "carol": {
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$GEdspTK4wAewdRUdkWuwAQ$a790zolKJP/OhYb8CWk3nmGOtk1PUDVeYIFlr70V7IA",
        "role": "hr"
    },
    "david": {
        "password_hash":  "$argon2id$v=19$m=65536,t=3,p=4$NpYeG6+jT5xut7txLNOeGQ$bjJ4md0339kWTNi9wn1DRWJ/qr0er+B1XqFFJL/ws+Q",
        "role": "engineering"
    },
    "eve": {
        "password_hash":"$argon2id$v=19$m=65536,t=3,p=4$XqKZhlUrK09TC8djuRBQPA$Q5XiStnSL+srFibNc+96jyGl5IiUrUZl7IVv1u/k0DM",
        "role": "executive"
    },
    "john": {
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$ZeY13vfy83EvzqBXkuUp0A$hL4wnuSuIGYnUvW1l5lQQL8wctw+ym3mYdZBW/8WQFc",
        "role": "employee"
    }
}

def authenticate_user(username: str, password: str):

    user = USERS.get(username)

    if not user:
        return None

    if not password_hash.verify(
        password,
        user["password_hash"]
    ):
        return None

    return {
        "username": username,
        "role": user["role"]
    }


def create_access_token(username: str, role: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

if __name__ == "__main__":

    user = authenticate_user(
        "alice",
        "alice123"
    )

    if user:
        token = create_access_token(
            user["username"],
            user["role"]
        )

        print("Token generated successfully")

        verified_user = verify_access_token(token)

        print("Verified user:")
        print(verified_user)

if __name__ == "__main__":
    result = authenticate_user("alice", "alice123")
    print(result)