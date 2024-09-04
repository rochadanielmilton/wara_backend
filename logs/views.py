from rest_framework import filters,generics, permissions
from logs.models import UserAction
from logs.serializers import UserActionSerializer

class UserActionsViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAction.objects.all()
    serializer_class = UserActionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']
    ordering = ['id']