from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from microface import microface
from .serializers import FailDelete,SuccessDelete


class FileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        # print(request.FILES['file'])
        face_result = microface.deleteFace(request.data['emp_code'])
        # print(face_result)
        if not face_result[0] == 0:
            data = { "ret_code" : face_result[0] , "msg" : face_result[1] }
            return Response(FailDelete(data).data, status=200)
        else:
            data = { "ret_code" : face_result[0] , "msg" : face_result[1] }
            return Response(SuccessDelete(data).data, status=200)