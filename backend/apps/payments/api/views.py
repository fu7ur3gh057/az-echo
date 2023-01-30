from datetime import datetime
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apps.payments.api.serializers import SubscriptionSerializer
from apps.payments.models import Subscription


class SubscriptionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_queryset(self):
        customer = self.request.user.customer
        subscriptions = self.queryset.filter(customer=customer).order_by('created_at')
        return subscriptions


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_subscription(request: Request):
    customer = request.user.customer
    for sub in customer.subscriptions.all():
        if sub.type == 1:
            return Response('Subscription is already active')
    subscription = Subscription.objects.create(customer=customer, type=1)
    subscription.save()
    return Response('Subscribe successful', status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def cancel_subscription(request: Request):
    customer = request.user.customer
    today = datetime.today().date()
    # Comparing customer and type is Active
    subscription = Subscription.objects.filter(Q(customer=customer) & Q(type=1)).first()
    if subscription is None:
        return Response('There arent any active subscriptions', status=status.HTTP_200_OK)
    subscription.canceled = True
    subscription.type = 3
    subscription.save()
    return Response('Subscription is canceled', status=status.HTTP_200_OK)
