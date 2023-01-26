from django.contrib import admin

from apps.crawlers.models import Echo, Driller


class EchoAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'customer_name', 'discover_interval', 'extract_interval', 'status', 'created_at']
    list_display_links = ['customer_name', 'status']

    # def repository_name(self, obj):
    #     return obj.repository


class DrillerAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'customer_name', 'interval', 'status', 'created_at']
    list_display_links = ['customer_name', 'status']

    # def repository_name(self, obj):
    #     return obj.repository


admin.site.register(Echo, EchoAdmin)
admin.site.register(Driller, DrillerAdmin)
