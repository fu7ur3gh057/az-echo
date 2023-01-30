from django.urls import path
from .views import cancel_subscription, SubscriptionListAPIView, create_subscription

urlpatterns = [
    path('', SubscriptionListAPIView.as_view(), name='all'),
    path('create/', create_subscription, name='create'),
    path('cancel/', cancel_subscription, name='cancel'),
]
