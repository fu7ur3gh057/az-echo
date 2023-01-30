from rest_framework import serializers

from apps.payments.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj.type == 1:
            return 'Active'
        elif obj.type == 2:
            return 'Expired'
        else:
            return 'Canceled'

    class Meta:
        model = Subscription
        fields = [
            'customer',
            'type',
            'expire_date',
            'canceled',
            'created_at'
        ]
