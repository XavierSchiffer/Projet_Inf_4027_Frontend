from rest_framework import serializers

class NonAdminUserCountSerializer(serializers.Serializer):
    state = serializers.CharField(default="SUCCES")
    results = serializers.ListField(
        child=serializers.DictField()
    )