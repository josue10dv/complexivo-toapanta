from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrdersViewSet, TableViewSet


router = DefaultRouter()
router.register(r"tables", TableViewSet, basename="tables")
router.register(r"orders", OrdersViewSet, basename="orders")

urlpatterns = []
urlpatterns += router.urls