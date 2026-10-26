from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from microface import microface
from .serializers import FailMatch, SuccessMatch,ListOfUsers
from m1cr0face.settings import ALLOWED_MAC_ADDRESSES, ALLOWED_HOSTS, GET_EMPLOYEE_DETAILS



class FileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        print(request.META['HTTP_MAC_ADDRESS'])
        mac_address = request.META['HTTP_MAC_ADDRESS'].strip()
        if (mac_address in ALLOWED_MAC_ADDRESSES):
            face_result = microface.findFace(request.FILES['file'])

            if not face_result[0] == 0:
                data = { "ret_code" : face_result[0] , "faces" : face_result[1] }
                return Response(FailMatch(data).data, status=200)

            else:
                emp_id = face_result[-1]
                get_employee_details = microface.getEmployeeDetails(GET_EMPLOYEE_DETAILS, emp_id=emp_id)

                data = {
                    "ret_code" : face_result[0],
                    "emp_code" : face_result[1],
                    "status_result" : get_employee_details
                }

                #==================================================================================================
                #       NOTE : Face getting recognised now, but saving face_recognised response in same log file
                #==================================================================================================

                microface.saveFailureResponse(api_name = 'detect_app_face_recognised', ret_code = face_result[0], msg = face_result[1], image = '')
                return Response(SuccessMatch(data).data, status=200)
        else:
            return Response(data={"message":"Not Allowed to access"}, status=401)

    def get(self, *args, **kwargs):
        face_result = microface.listOfUsers()
        data = { "ret_code" : face_result[0] , "users" : face_result[1] }
        return Response(ListOfUsers(data).data, status=200)
