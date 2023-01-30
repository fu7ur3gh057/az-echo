from rest_framework import serializers
from apps.synthesis.models import Synthesis
from apps.synthesis.utils import get_synthesis_status


class SynthesisSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_synthesis_status(status=obj.status)

    class Meta:
        model = Synthesis
        fields = [
            'id',
            'job_id',
            'repository',
            'link',
            'text',
            'lang',
            'crawled_status',
            'error_status',
            'created_at',
            'updated_at'
        ]
