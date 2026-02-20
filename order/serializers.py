from rest_framework import serializers
from .models import Orders, Tables

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tables
        fields = ["id", "name", "capacity", "is_available"]

class OrderSerializer(serializers.ModelSerializer):
    table_name = serializers.CharField(source="table_id.name", read_only=True)

    class Meta:
        model = Orders
        fields = ["id", "table_id", "table_name", "items_summary", "total", "state", "created_at"]