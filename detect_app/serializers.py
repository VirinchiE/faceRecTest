from rest_framework import serializers

class FailMatch(serializers.Serializer):
   ret_code = serializers.IntegerField()
   faces = serializers.CharField()

class SuccessMatch(serializers.Serializer):
    ret_code = serializers.IntegerField()
    emp_code = serializers.CharField()
    status_result = serializers.DictField()

class ListOfUsers(serializers.Serializer):
    ret_code = serializers.IntegerField()
    users = serializers.ListField(child=serializers.CharField(max_length=32, allow_blank=True))