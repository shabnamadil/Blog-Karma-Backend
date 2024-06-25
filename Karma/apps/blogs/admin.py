from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import (
    Blog, 
    Category, 
    Comment
)


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
        'show_comments_count',
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
    display_blog_author.short_description = 'Müəllif'

    def display_blog_img(self, obj):
        image = obj.blog_image.url
        if image:
            raw_html = f'<img style="width:70px;height:auto;" src="{image}">'
            return format_html(raw_html)
    display_blog_img.short_description = 'Cover foto'

    def display_blog_categories(self, obj):
        return ", ".join(category.category_name for category in obj.category.all())
    display_blog_categories.short_description = 'Kateqoriya'

    def show_comments_count(self, obj):
        result = Comment.objects.filter(blog=obj).count()
        return result
    show_comments_count.short_description = 'RƏYLƏRİN SAYI'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'get_comment', 'display_blog',
        'display_comment_author', 
        'status', 'created_date',
    )
    list_filter = (
        'published_at', 'status'
    )
    search_fields = (
        'comment_text',
    )
    ordering = ('-updated_at', 'comment_text')
    date_hierarchy = 'published_at'
    list_per_page = 20
    actions =(make_draft, make_published)
    readonly_fields = ('comment_author', 'comment_slug')
    autocomplete_fields = ('blog', )
    exclude = ('published_at', )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.comment_author = request.user
        super().save_model(request, obj, form, change)

    def display_blog(self, obj):
        url = reverse("admin:blogs_blog_change", args=[obj.blog.id])
        link = '<a style="color: blue;" href="%s">%s</a>' % (
            url, 
            obj.blog.blog_title
        )
        return mark_safe(link)
    display_blog.short_description = 'Bloq'

    def display_comment_author(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.comment_author.id])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.comment_author.get_full_name()
        )
        return mark_safe(link)
    display_comment_author.short_description = 'Müəllif'

    def get_comment(self, obj):
        return obj.truncated_comment
    get_comment.short_description = 'Comment'


admin.site.register(Category)
