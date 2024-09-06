from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions
from appointments.api.test_and_results.serializers import TestAndResultSerializer
from appointments.models import TestAndResultModel
from utils.permissions import IsAdmin, IsStaff


class TestAndResultView(ModelViewSet):
    queryset = TestAndResultModel.objects.all()
    serializer_class = TestAndResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin|IsStaff]

    # parser_classes = [MultiPartParser,FormParser]


# {
#     "appointment": 40,
#     "test_type": "ECG",
#     "test_name": "Complete Blood Count",
#     "test_fees_paid_token": "TOKEN2",
#     "test_result_available": false,

#     "notes": "Patient fasting for 12 hours prior to test.",
#     "report_file": null
# }
