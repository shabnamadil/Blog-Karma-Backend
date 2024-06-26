from django.utils.safestring import mark_safe

from rest_framework import serializers

from apps.core.models import (
    ContactInformation,
    AboutUs,
    ContactMessage
)


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = (
            'id',
            'location',
            'number',
            'email',
            'linkedin',
            'facebook',
            'instagram',
            'whatsapp'
        )


class AboutUsInformationSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    class Meta:
        model = AboutUs
        fields = (
            'id',
            'company_name',
            'content'
        )

    def get_content(self, obj):
        return mark_safe(obj.content)


class ContactMessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = (
            'id',
            'message_by',
            'subject',
            'message'
        )

    def validate(self, attrs):
        request = self.context.get('request')
        if request.user.is_authenticated:
            attrs['message_by'] = request.user.get_full_name()
        return super().validate(attrs)