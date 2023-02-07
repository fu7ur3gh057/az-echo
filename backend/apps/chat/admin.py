from django.contrib import admin

from apps.chat.models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_display_links = ['user', 'date']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'text', 'date']
    list_display_links = ['room', 'sender']


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
