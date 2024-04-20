from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
import xml.etree.ElementTree as ET
from .models import User

class UserAPIView(APIView):
    def post(self, request):
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = User.objects.create_user(
            name=name,
            email=email,
            password=password
        )

        response = HttpResponse(content_type='text/xml')
        response_xml = ET.Element('response')

        ET.ElementTree(response_xml).write(response)
        return response
