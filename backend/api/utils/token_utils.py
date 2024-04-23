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
        expiration_time = self._set_expiration_time(
            token_type=self.__name__, creation_time=creation_time, user_id=user.id
        )
        payload = {
            "token_type": self.__name__,
            "user_id": user.id,
            "created": creation_time.isoformat(),
            "expired": expiration_time.isoformat(),
        }
        self.value = encode(payload, KEY, algorithm="HS256")

    @classmethod
    def check(self: Self) -> User | int:
        try:
            decoded_content = decode(self.value, KEY, algorithms=["HS256"])
        except Exception:
            return -1
        expiration_time_str = decoded_content.get("expired")
        if expiration_time_str:
            expiration_time = datetime.strptime(
                expiration_time_str, "%Y-%m-%dT%H:%M:%S.%f"
            )
            if datetime.utcnow() > expiration_time:
                return -3  # Token expired

        real_type = decoded_content.get("token_type")
        if self.__name__ != real_type:
            return -1  # Token invalid

        user_id = decoded_content.get("user_id")
        creation_date_str = decoded_content.get("created")
        user = authenticate_user(user_id=user_id)
        if user:
            if self.__name__ == "RefreshToken":
                return self._validate_refresh_token(
                    user=user, creation_date_str=creation_date_str
                )
            elif self.__name__ == "AccessToken":
                return user  # Token valid

        return -1  # Token invalid

    def _set_expiration_time(
        token_type: str, creation_time: datetime, user_id: int
    ) -> datetime:
        if token_type.startswith("A"):  # Access token
            expiration_time = creation_time + timedelta(
                minutes=settings.ACCESS_TOKEN_PERIOD
            )
        elif token_type.startswith("R"):  # Refresh token
            expiration_time = creation_time + timedelta(
                days=settings.REFRESH_TOKEN_PERIOD
            )
            session_update(creation_time=creation_time, user_id=user_id)
        else:
            raise Exception(f"Invalid token_type given = {token_type}")
        return expiration_time

    def _validate_refresh_token(user: User, creation_date_str: str) -> None:
        try:
            session = Sessions.objects.get(user=user.id)
            session_created = session.created_at.strftime(format="%Y-%m-%dT%H:%M:%S.%f")
            if session_created == creation_date_str:
                return user  # Token valid
            else:
                return -2  # Token annulled
        except Sessions.DoesNotExist:
            creation_date = datetime.strptime(creation_date_str, "%Y-%m-%dT%H:%M:%S.%f")
            data = {"user": user, "created_at": creation_date}
            serializer = SessionsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return user  # Token valid
            else:
                return -1  # Token invalid

    def _type_check() -> bool:
        return ...


class RefreshToken(Token):
    value = str


class AccessToken(Token):
    value = str

    @classmethod
    def refresh(self: Self, refresh_token: RefreshToken) -> None | int:
        refresh_check = refresh_token.check()
        if refresh_check.__class__ != int:
            user = refresh_check
            access_token = AccessToken
            access_token.create(user=user)
            self.value = access_token.value
            return None
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
