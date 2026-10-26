from rest_framework import serializers

class FailDelete(serializers.Serializer):
   ret_code = serializers.IntegerField()
   msg = serializers.CharField()

class SuccessDelete(serializers.Serializer):
   ret_code = serializers.IntegerField()
   msg = serializers.CharField()
