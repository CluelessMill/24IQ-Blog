from django.test import TestCase
from django.urls import reverse
from icecream import ic
from rest_framework.test import APIClient

from .decorators.functions import test_function


class AuthAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def receive_tokens(self, mode:str):
        data = {"email": "admin", "password": "admin"}
        url = reverse(viewname=mode)
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(first=response.status_code, second=201)
        return response

    def test_auth(self) -> None:
        data = {"email": "admin", "password": "admin"}

        def test_sign_up(self) -> None:
            print("Sign_up test")
            url = reverse(viewname="sign-up")
            response = self.client.post(path=url, data=data, format="json")
            self.assertEqual(first=response.status_code, second=201)

        def test_sign_in(self) -> None:
            print("Sign_in test")
            data = {"email": "admin", "password": "admin"}
            url = reverse(viewname="sign-in")
            response = self.client.post(path=url, data=data, format="json")
            self.assertEqual(first=response.status_code, second=201)

        def test_refresh_token(self) -> None:
            print("Refresh_token test")
            response = self.receive_tokens(mode="sign-in")
            cookie_value = response.cookies["refreshToken"].value
            url = reverse(viewname="refresh-token")
            response = self.client.put(path=url, data=None, format="json")
            response.set_cookie("refreshToken", cookie_value)
            self.assertEqual(first=response.status_code, second=201)

        test_sign_up(self=self)
        test_sign_in(self=self)
        test_refresh_token(self=self)

    def test_roles(self) -> None:
        def test_get_roles(self) -> None:
            print("Get_roles test")
            token_request = self.receive_tokens(mode="sign-up")
            cookie_value = token_request.cookies["refreshToken"].value
            url = reverse(viewname="role-list")
            response = self.client.get(path=url, data=None, format="json")
            response.set_cookie("refreshToken", cookie_value)
            self.assertEqual(first=response.status_code, second=200)

        test_get_roles(self=self)