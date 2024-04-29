from ..models import User


def admin_check(user: User) -> bool | int:
    #TODO make this function word via access token
    return user.role == "admin"
