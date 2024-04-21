from datetime import datetime, timedelta
from typing import Self

from django.conf import settings
from jwt import decode, encode

from ..models import Sessions, User
from ..serializers import SessionsSerializer
from .session_utils import session_update
from .user_utils import authenticate_user

KEY = settings.JWT_KEY


class Token:
    @classmethod
    def __init__(self: Self, token_value: str) -> None:
        self.value = token_value

    @classmethod
    def create(self: Self, user: User) -> None:
        creation_time = datetime.utcnow()
        if self.__name__ == "AccessToken":
            expiration_time = creation_time + timedelta(
                minutes=settings.ACCESS_TOKEN_PERIOD
            )
        elif self.__name__ == "RefreshToken":
            expiration_time = creation_time + timedelta(
                days=settings.REFRESH_TOKEN_PERIOD
            )
            session_error = session_update(
                creation_time=creation_time, user_id=user.id
            )
            if session_error is not None:
                raise (session_error)
        else:
            raise Exception("Invalid token_type")
        payload = {
            "token_type": self.__name__,
            "user_id": user.id,
            "created": creation_time.isoformat(),
            "expired": expiration_time.isoformat(),
        }
        self.value = encode(payload, KEY, algorithm="HS256")

    @classmethod
    def check(self: Self) -> User | int:
        decoded_content = decode(self.value, KEY, algorithms=["HS256"])
        expiration_time_str = decoded_content.get("expired", None)
        expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%dT%H:%M:%S.%f")
        real_type = decoded_content.get("token_type", None)

        if expiration_time is not None and datetime.utcnow() > expiration_time:
            return -3  # Token expired

        if self.__name__ != real_type:  # Type check
            return -1  # Token invalid

        user_id = decoded_content.get("user_id", None)
        creation_date_str = decoded_content.get("created", None)
        creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        user = authenticate_user(user_id=user_id)
        if user is not None:
            if self.__name__ == "RefreshToken":
                try:
                    session = Sessions.objects.get(user=user_id)
                    session_created_iso = session.created_at
                    session_created = session_created_iso.strftime(
                        format="%Y-%m-%d %H:%M:%S.%f"
                    )
                    if str(session_created) == str(creation_date):
                        return user  # Token valid
                    else:
                        return -2  # Token annulled
                except Sessions.DoesNotExist:
                    data = {"user": user_id, "created_at": creation_date}
                    serializer = SessionsSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return user  # Token valid
                    else:
                        return -1  # Token invalid
            elif self.__name__ == "AccessToken":
                return user  # Token valid
            else:
                return -1  # Token invalid
        else:
            return -1  # Token invalid


class RefreshToken(Token):
    value = str


class AccessToken(Token):
    value = str

    @classmethod
    def refresh(self: Self, refresh_token: RefreshToken) -> None | Exception:
        refresh_check = refresh_token.check()
        access_check = self.check()
        if refresh_check.__class__ != int:
            if access_check != -1:
                user = refresh_check
                access_token = AccessToken
                access_token.create(user=user)
                self = access_token
                return None
            else:
                return access_check
        else:
            return refresh_check


def check_res_to_error(result_code: int) -> str:
    error_message = ""
    match result_code:
        case -3:
            error_message = "Token is expired"
        case -1:
            error_message = "Token is invalid"
        case -2:
            error_message = "Token was annulled"
    return error_message
