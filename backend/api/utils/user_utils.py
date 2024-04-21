from hashlib import sha256

from ..models import User
from .cript_utils import check_password, decrypt, encrypt


def authenticate_user(nickname=None, user_id=None, password=None, email=None):
    try:
        user = None
        if nickname is not None and password is not None:
            user = User.objects.get(nickname=encrypt(nickname))
            if not check_password(input_password=password, stored_password=user.password.tobytes()):
                user = None
        elif email is not None and password is not None:
            user = User.objects.get(email=encrypt(email))
            if not check_password(input_password=password, stored_password=user.password.tobytes()):
                user = None
        elif nickname is None and email is None:
            user = User.objects.get(user_id=user_id)

        if not user:
            return None
        user.nickname = decrypt(user.nickname.tobytes())
        user.email = decrypt(user.email.tobytes())
        return user
    except User.DoesNotExist:
        return None


def check_user(nickname, password):
    try:
        user = User.objects.get(nickname=encrypt(nickname))
        return check_password(password, user["password"])
    except User.DoesNotExist:
        return False


def check_is_unique(nickname=None, email=None):
    if email is not None:
        try:
            User.objects.get(email=encrypt(email))
            return False
        except User.DoesNotExist:
            return True
    else:
        try:
            User.objects.get(nickname=encrypt(nickname))
            return False
        except User.DoesNotExist:
            return True


def generate_nickname(email):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    hashed_email = sha256(email.encode()).hexdigest()
    hashed_email = [(chr(int(i) + 97) if i.isdigit() else i) for i in hashed_email]
    nickname = ""
    for char in hashed_email:
        if len(nickname) >= 15:
            break
        if char in consonants:
            nickname += char
            if len(nickname) < 15:
                nickname += vowels[int(ord(char)) % len(vowels)]
        elif char in vowels:
            nickname += consonants[int(ord(char)) % len(consonants)]
    while len(nickname) < 15:
        nickname += consonants[int(hashed_email[0], 16) % len(consonants)]

    return nickname
