from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.html import format_html
from django.contrib.auth import get_user_model

from apps.users.models import (
    Profile
)
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm,
    ProfileForm
)

User = get_user_model()


@admin.action(description="Mark selected items as active")
def make_active(self, request, queryset):
    queryset.update(active=True)

@admin.action(description="Mark selected items as deactive")
def make_inactive(self, request, queryset):
    queryset.update(active=False)


class ProfileInline(admin.TabularInline):
    model = Profile
    form = ProfileForm
    

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'user_full_name', 'email', 'display_profession', 
        'display_user_img', 'get_groups', 'is_active', 
        'is_staff', 'is_superuser'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 
        'user_profile__profession', 'groups'
    )
    fieldsets = (
        ('Main Information', {'fields': (
            'first_name', 'last_name', 'password'
        )}),
        ('Permissions', {'fields': (
            'is_staff', 'is_active','is_superuser', 
            'groups', 'user_permissions'
        )}),
        ('Important Dates', {'fields': (
            'last_login', 'date_joined'
        )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name', 'email',
                'password1', 'password2'
        )}),
    )
    search_fields = (
        'email', 'first_name', 'last_name', 
        'user_profile__profession', 'groups__name'
    )
    autocomplete_fields = ('groups',)
    ordering = ('first_name', 'last_name')
    inlines = (ProfileInline,)

    def display_user_img(self, obj):
        image = obj.user_profile.image.url if obj.user_profile.image else None
        if image:
            raw_html = f'<img style="width:70px;height:auto;" src="{image}">'
            return format_html(raw_html)
    display_user_img.short_description = 'Image'

    def display_profession(self, obj):
        return obj.user_profile.profession if obj.user_profile else None
    display_profession.short_description = 'Profession'

    def get_groups(self, obj):
        user_groups = []
        for group in obj.groups.all():
            user_groups.append(group)
        return user_groups
    get_groups.short_description = 'Groups'


admin.site.register(User, CustomUserAdmin)

admin.site.index_title = 'Admin Panel'
admin.site.site_title = 'Karma'
admin.site.site_header = 'Karma'
