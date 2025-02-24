from rest_framework import serializers

class AdminUserCountSerializer(serializers.Serializer):
    state = serializers.CharField(default="SUCCES")
    results = serializers.ListField(
        child=serializers.DictField()
    )