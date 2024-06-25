from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    ContactInformation,
    AboutUs,
    ContactMessage
)

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('location', 'number', 'email')
    search_fields = ('location', 'number', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'get_content', 'updated_at')
    search_fields = ('company_name', 'content')
    readonly_fields = ('created_at', 'updated_at')

    def get_content(self, obj):
        return obj.truncated_content
    get_content.short_description = 'Haqqımızda'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('get_message', 'subject', 'message_by', 'created_at')
    list_filter = ('created_at', )
    search_fields = ('message', 'subject')
    list_per_page = 20
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('message_by', 'created_at')

    def get_message(self, obj):
        return obj.truncated_message
    get_message.short_description = 'Mesaj'
