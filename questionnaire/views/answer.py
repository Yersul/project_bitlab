from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from questionnaire.models import Answer
from questionnaire.serializers import AnswerSerializer


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = AnswerSerializer
