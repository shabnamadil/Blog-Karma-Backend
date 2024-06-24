from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import (
    IP, 
    Blog, 
    Category, 
    Comment
)

admin.site.register(Category)
admin.site.register(Comment)


@admin.action(description="Mark selected items DRAFT")
def make_draft(self, request, queryset):
    queryset.update(status=Blog.Status.DRAFT)

@admin.action(description="Mark selected items PUBLISHED")
def make_published(self, request, queryset):
    queryset.update(status=Blog.Status.PUBLİSHED)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'blog_title', 'display_blog_img',
        'display_blog_author', 'view_count',
        'display_blog_categories', 
        'status', 'created_date',
    )
    list_filter = (
        'published_at', 'status',
        'category'
    )
    search_fields = (
        'blog_title', 'blog_content', 
        'category__category_name',
        'category'
    )
    ordering = ('-updated_at', 'blog_title')
    date_hierarchy = 'published_at'
    list_per_page = 20
    actions =(make_draft, make_published)
    readonly_fields = ('author', 'slug')
    exclude = ('published_at', )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def display_blog_author(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.author.id])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.author.get_full_name()
        )
        return mark_safe(link)
    display_blog_author.short_description = 'Bloq müəllifi'

    def display_blog_img(self, obj):
        image = obj.blog_image.url
        if image:
            raw_html = f'<img style="width:70px;height:auto;" src="{image}">'
            return format_html(raw_html)
    display_blog_img.short_description = 'Cover foto'

    def display_blog_categories(self, obj):
        return ", ".join(category.category_name for category in obj.category.all())
    display_blog_categories.short_description = 'Category'
