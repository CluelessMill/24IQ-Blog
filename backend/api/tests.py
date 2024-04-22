from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class SignUpAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_signup_get_request(self) -> None:
        url = reverse(viewname='sign-up')
        response = self.client.get(path=url)
        self.assertEqual(first=response.status_code, second=200)

class SignInAPITest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_signin_post_request(self) -> None:
        data = {
            "email": "admin",
            "password": "admin"
        }
        url = reverse(viewname='sign-up')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(first=response.status_code, second=201)


