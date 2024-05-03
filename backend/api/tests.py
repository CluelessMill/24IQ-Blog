from cgi import test
from django.test import TestCase
from django.urls import reverse
from icecream import ic
from rest_framework.test import APIClient

from .decorators.functions import test_function


class AuthAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def _receive_tokens(self, mode: str):
        data = {"email": "admin", "password": "admin"}
        url = reverse(viewname=mode)
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)
        return response

    def _set_role_DEBUG(self, new_role: str, nickname: str):
        url = reverse(viewname="role-set-deb")
        data = {"role": new_role, "nickname": nickname}
        response = self.client.put(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)

    def test_auth(self) -> None:
        data = {"email": "admin", "password": "admin"}

        def test_sign_up(self) -> None:
            print("Sign_up test")
            url = reverse(viewname="sign-up")
            response = self.client.post(path=url, data=data, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_sign_in(self) -> None:
            print("Sign_in test")
            url = reverse(viewname="sign-in")
            response = self.client.post(path=url, data=data, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_refresh_token(self) -> None:
            print("Refresh_token test")
            response = self._receive_tokens(mode="sign-in")
            cookie_value = response.cookies["refreshToken"].value
            url = reverse(viewname="refresh-token")
            response = self.client.put(path=url, data=None, format="json")
            response.set_cookie("refreshToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        test_sign_up(self=self)
        test_sign_in(self=self)
        test_refresh_token(self=self)

    def test_roles(self) -> None:
        nickname, cookie_value = None, None

        def init_profile(self, mode):
            token_request = self._receive_tokens(mode=mode)
            nickname = token_request.data["user"]["nickname"]
            cookie_value = token_request.cookies["accessToken"].value
            return nickname, cookie_value

        def test_role_set(self, nickname, cookie_value) -> None:
            print("Role set test")
            url = reverse(viewname="role-set")
            data = {"role": "user", "nickname": nickname}

            print("No permission")
            response = self.client.put(path=url, data=data, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=400)

            print("With permission")
            self._set_role_DEBUG(new_role="admin", nickname=nickname)
            nickname, cookie_value = init_profile(self=self, mode="sign-in")
            data = {"role": "user", "nickname": nickname}
            response = self.client.put(path=url, data=data, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=201)

        def test_role_list(self, nickname, cookie_value) -> None:
            print("Roles list test")
            url = reverse(viewname="role-list")

            print("No permission")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=400)

            print("With permission")
            self._set_role_DEBUG(new_role="admin", nickname=nickname)
            response = self.client.get(path=url, data=None, format="json")
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)

        def test_is_admin(self, nickname, cookie_value) -> None:
            print("Is admin test")
            url = reverse(viewname="is-admin")

            print("Admin")
            nickname, cookie_value = init_profile(self=self, mode="sign-in")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)
            self.assertEqual(first=response.data["isAdmin"], second=True)

            print("User")
            self._set_role_DEBUG(new_role="user", nickname=nickname)
            nickname, cookie_value = init_profile(self=self, mode="sign-in")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("accessToken", cookie_value)
            ic(response.data)
            self.assertEqual(first=response.status_code, second=200)
            self.assertEqual(first=response.data["isAdmin"], second=False)

        nickname, cookie_value = init_profile(self=self, mode="sign-up")
        test_role_set(self=self, nickname=nickname, cookie_value=cookie_value)
        test_role_list(self=self, nickname=nickname, cookie_value=cookie_value)
        test_is_admin(self=self, nickname=nickname, cookie_value=cookie_value)

    def test_posts(self):
        def test_receive_posts(self):
            pass

        def test_create_post(self):
            pass


        pass
