from rest_framework import serializers

class LearnResult(serializers.Serializer):
   ret_code = serializers.IntegerField()
   msg = serializers.CharField()
