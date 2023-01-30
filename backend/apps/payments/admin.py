from django.contrib import admin

from apps.payments.models import Subscription, SubscriptionChecker


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["customer", "type", "expire_date", "created_at"]
    list_display_links = ["customer", "expire_date"]
    list_filter = ["customer", "type"]


class SubscriptionCheckerAdmin(admin.ModelAdmin):
    list_display = ['interval', 'status']
    list_display_links = ['status']


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionChecker, SubscriptionCheckerAdmin)
