from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from microface import microface
from .serializers import LearnResult

class FileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        face_result = microface.newFace(request.FILES['file'],request.data['emp_code'])
        data = { "ret_code" : face_result[0] , "msg" : face_result[1] }
        return Response(LearnResult(data).data, status=200)