import json
import requests
import time
import csv
import os
from datetime import date
from django.shortcuts import render
from microface import microface
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from m1cr0face.settings import UPDATED_CHECKIN_CHECKOUT_NODE_URL,ALLOWED_MAC_ADDRESSES,ALLOWED_HOSTS
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime


class FileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        mac_address = request.META['HTTP_MAC_ADDRESS'].strip()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        employee_id = body['employee_id']
        node_url = UPDATED_CHECKIN_CHECKOUT_NODE_URL
        print(f">>>> type (deviceId) == {mac_address} and type(employee_Id) == {employee_id}")
        if (mac_address in ALLOWED_MAC_ADDRESSES):
            request_body = {
                "deviceId": mac_address,
                "employee_Id": employee_id
            }
            try : 
                print(f">>>> node_url == {node_url}\nrequest_body =={request_body} ")

                response = requests.post(url=node_url,json=request_body,timeout=30)
                print(f">>> response == {response}")
                if response != None and response != "":
                    response_body_unicode = response.content.decode('utf-8')
                    response_body = json.loads(response_body_unicode)
                    microface.saveNodeLog(api_name = 'checkin_checkout_app', emp_id = employee_id, request_obj = employee_id, response_obj = response_body )
                    print(response_body)
                    return Response(data=response_body, status=200)

            except Exception as error:
                print("Request Failed, Node Server Error == [", error, "]")
                microface.saveNodeLog(api_name = 'checkin_checkout_app', emp_id = employee_id, request_obj = employee_id, error = error)
                return Response(data={"status_message": "Node Api Call Failed","status_code":"2002"}, status=200)


        else:
            return Response(data={"message": "Not Allowed to access"}, status=401)
