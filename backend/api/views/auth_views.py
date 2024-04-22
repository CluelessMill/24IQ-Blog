from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from ..decorators.response import response_handler
from ..serializers import UserSerializer
from ..utils.cript_utils import decrypt
from ..utils.request_utils import check_not_none
from ..utils.token_utils import AccessToken, RefreshToken, check_res_to_error
from ..utils.user_utils import authenticate_user, check_is_unique, generate_nickname


class SignInAPIView(APIView):
    # @response_handler
    def post(self, request):
        password = request.data.get("password", "")
        nickname = request.data.get("nickname", "")
        email = request.data.get("email", "")

        if not nickname:
            nickname = None
            check_not_none(password, email)
        if not email:
            email = None
            check_not_none(password, nickname)

        user = authenticate_user(nickname=nickname, password=password, email=email)
        if user:
            profile_img = user.profile_img
            access_token, refresh_token = AccessToken, RefreshToken
            access_token.create(user=user)
            refresh_token.create(user=user)
            response_data = {
                "accessToken": access_token.value,
                "user": {
                    "email": user.email,
                    "nickname": user.nickname,
                    "avatarPath": profile_img,
                    "isAdmin": False,
                    "isActive": True,
                },
            }
            response = JsonResponse(data=response_data, status=201)
            response.set_cookie(key="refreshToken", value=refresh_token.value)
            return response  # Return access and refresh token
        else:
            # Return authentication error
            return Response(
                f"Invalid {'nickname' if not email else 'email'} or password.",
                status=400,
            )


class SignUpAPIView(APIView):
    @response_handler
    def get(self, request):
        users = User.objects.all()
        response_data = []
        for user in users:
            response_data.append(
                {
                    "id": user.id,
                    "email": decrypt(data=user.email.tobytes()),
                    "nickname": decrypt(data=user.nickname.tobytes()),
                    "password": user.password.tobytes(),
                    "info": user.info,
                    "role": user.role,
                    "active": user.active,
                    "profile_img": user.profile_img,
                }
            )
        return Response(response_data)

    # @response_handler
    def post(self, request):
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        check_not_none(password, email)

        if not email:
            return Response("Not enough data", status=400)  # Return error
        if not check_is_unique(email=email):
            return Response("Email already exists", status=400)

        nickname = generate_nickname(email)

        input_data = {
            "nickname": nickname,
            "email": email,
            "password": password,
        }
        serializer = UserSerializer(data=input_data)
        if serializer.is_valid():
            user = serializer.save()
            profile_img = user.profile_img
            access_token, refresh_token = AccessToken, RefreshToken
            access_token.create(user=user)
            refresh_token.create(user=user)
            response_data = {
                "accessToken": access_token.value,
                "user": {
                    "email": email,
                    "nickname": nickname,
                    "avatarPath": profile_img,
                    "isAdmin": False,
                    "isActive": True,
                },
            }
            response = JsonResponse(data=response_data, status=201)
            response.set_cookie(key="refreshToken", value=refresh_token.value)
            return response
        else:
            return Response("An error occurred", status=400)


class UpdateTokenAPIView(APIView):
    @response_handler
    def post(self, request):
        access_token_req = request.data.get("accessToken", "")
        refresh_token_req = request.COOKIES.get("token")
        check_not_none(access_token_req, refresh_token_req)

        access_token = AccessToken(token_value=access_token_req)
        refresh_token = RefreshToken(token_value=refresh_token_req)
        error = access_token.refresh(refresh_token)
        if error:
            return Response(check_res_to_error(error), status=400)
        else:
            return Response({"accessToken": access_token.value}, status=201)
