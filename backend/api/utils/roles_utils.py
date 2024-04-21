from .token_utils import AccessToken


def admin_check(token: AccessToken) -> bool:
    user = token.check()
    if (user.__class__ != int) and (user.role == "admin"):
        return True
    else:
        return False
