from django.contrib import admin

from apps.synthesis.models import Synthesis, Generator


class SynthesisAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'link_preview', 'text_preview', 'lang', 'crawled_status', 'error_status']
    list_display_links = ['link_preview', 'lang']

    def text_preview(self, obj):
        return f'{obj.text[0:80]}...'

    def link_preview(self, obj):
        return f'{obj.link[0:50]}...'


class GeneratorAdmin(admin.ModelAdmin):
    list_display = ['interval', 'status', 'created_at']
    list_display_links = ['interval']


admin.site.register(Synthesis, SynthesisAdmin)
admin.site.register(Generator, GeneratorAdmin)
