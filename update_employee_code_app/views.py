from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import os
import time

# Create your views here.

class FileView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self,request):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("start time")
        print(current_time)
        old_employee_code = request.GET['old_employee_code']
        new_employee_code = request.GET['new_employee_code']
        myData = (old_employee_code,new_employee_code)
        # search in file with old employee code
        # now update the filename with bew employee code
        facefile = 'known_faces/'
        for f in os.listdir(facefile):
            # print(">>> matched with == ",f.split("_")[1] )
            if(f.split("_")[1] == old_employee_code):
                print(">>>Matched user == ",f)
                new_employee_code=f.split("_")[0]+"_"+new_employee_code
                os.rename(facefile+f, facefile+new_employee_code)
                t = time.localtime()
                end_time = time.strftime("%H:%M:%S", t)
                print("end time")
                return Response(data={"ret_code":0,"status_message":"Updated the Employee code" }, status=200)