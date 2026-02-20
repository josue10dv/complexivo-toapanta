from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .mongo import db
from .mongo_serializers import MenuSerializer, OrderEventSerializer

class MenuViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = list(db.menus.find())
        serializer = MenuSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data['created_at'] = datetime.utcnow()
            result = db.menus.insert_one(data)
            data['_id'] = str(result.inserted_id)
            return Response(MenuSerializer(data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderEventListView(APIView):
    def get(self, request):
        order_id_param = request.query_params.get('order_id')
        if not order_id_param:
            return Response({"error": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order_id = int(order_id_param)
            events = list(db.order_events.find({"order_id": order_id}).sort("created_at", -1))
            serializer = OrderEventSerializer(events, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "order_id must be integer"}, status=status.HTTP_400_BAD_REQUEST)
