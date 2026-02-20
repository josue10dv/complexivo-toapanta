from rest_framework import serializers

class MenuSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=50)
    price = serializers.FloatField()
    is_available = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)

class OrderEventSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    order_id = serializers.IntegerField()
    event_type = serializers.CharField(max_length=50)
    source = serializers.CharField(max_length=20)
    note = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
