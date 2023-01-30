import django_filters
import magic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.synthesis.api.serializers import SynthesisSerializer
from apps.synthesis.api.voicen_api import get_synthesis_audio
from apps.synthesis.models import Synthesis
from apps.synthesis.pagination import SynthesisPagination


class SynthesisFilter(django_filters.FilterSet):
    lang = django_filters.CharFilter(field_name='lang', lookup_expr='iexact')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='iexact')
    char_count = django_filters.NumberFilter()
    char_count__gt = django_filters.NumberFilter(field_name="char_count", lookup_expr="gt")
    char_count__lt = django_filters.NumberFilter(field_name="char_count", lookup_expr="lt")

    class Meta:
        model = Synthesis
        fields = ['lang', 'status', 'char_count']


class SynthesisListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SynthesisSerializer
    queryset = Synthesis.objects.all()
    pagination_class = SynthesisPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SynthesisFilter
    search_fields = ['lang', 'status']

    def get_queryset(self):
        user = self.request.user
        repo = user.customer.repository
        synthesis_list = self.queryset.filter(repository=repo).order_by('-created_at')
        return synthesis_list


class SynthesisAPIView(APIView):
    serializer_class = SynthesisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, synthesis_id):
        pass

    def put(self, request: Request, synthesis_id):
        pass

    def post(self, request: Request):
        pass

    def delete(self, request: Request, synthesis_id):
        pass


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def play_synthesis_audio(request: Request):
    try:
        link = request.query_params['link']
        synthesis = Synthesis.objects.filter(link=link).first()
        if synthesis is not None:
            content = get_synthesis_audio(job_id=synthesis.job_id)
            mime_type = magic.from_buffer(content, mime=True)
            response = HttpResponse()
            response.write(content)
            response['Content-Type'] = mime_type
            response['Accept-Ranges'] = 'bytes'
            return response
        else:
            return Response('Synthesis job not found', status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        print(ex)
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)
