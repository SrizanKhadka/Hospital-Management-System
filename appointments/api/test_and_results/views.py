from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from appointments.api.test_and_results.serializers import TestAndResultSerializer
from appointments.models import TestAndResultModel
from utils.permissions import IsAdmin, IsStaff


class TestAndResultView(ModelViewSet):
    queryset = TestAndResultModel.objects.all()
    serializer_class = TestAndResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin, IsStaff]
