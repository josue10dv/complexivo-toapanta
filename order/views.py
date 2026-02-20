from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime
from .models import Tables, Orders
from .serializers import TableSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly
from .mongo import db

class TableViewSet(viewsets.ModelViewSet):
    queryset = Tables.objects.all().order_by("id")
    serializer_class = TableSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.select_related("table_id").all().order_by("-id")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["table_id", "state"]
    search_fields = ["items_summary", "state", "table_id__name"]
    ordering_fields = ["id", "state", "total", "created_at"]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['post'], url_path='events')
    def create_event(self, request, pk=None):
        order = self.get_object()
        event_type = request.data.get('event_type')
        source = request.data.get('source', 'SYSTEM')
        note = request.data.get('note', '')

        EVENT_TO_STATE_MAP = {
            "SENT_TO_KITCHEN": "in_process",
            "SERVED": "served",
            "PAID": "paid",
            "CANCELLED": "cancelled",
        }

        if not event_type:
            return Response({"error": "event_type is required"}, status=status.HTTP_400_BAD_REQUEST)

        new_state = EVENT_TO_STATE_MAP.get(event_type)
        if new_state:
            order.state = new_state
            order.save()

        event_document = {
            "order_id": order.id,
            "event_type": event_type,
            "source": source,
            "note": note,
            "created_at": datetime.utcnow()
        }
        db.order_events.insert_one(event_document)

        return Response(
            {"status": "event created", "order_new_state": order.state},
            status=status.HTTP_201_CREATED
        )
