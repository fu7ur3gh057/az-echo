from django.contrib import admin

from apps.customers.models import Customer, Repository


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'name']
    list_display_links = ['pkid', "name"]


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'customer', 'blacklist_size', 'created_at']
    list_display_links = ['pkid', "customer"]

    def blacklist_size(self, obj):
        return len(obj.blacklist)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Repository, RepositoryAdmin)
