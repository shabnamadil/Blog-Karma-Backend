from rest_framework import serializers

from apps.blogs.models import (
    Blog,
    Category,
    Comment
)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'category_name'
        )

class CommentListSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'updated_date',
            'created_date'
        )

    def get_comment_author(self, obj):
        if obj.comment_author.get_full_name():
            return obj.comment_author.get_full_name()
        return 'Admin User'
    

class CommentPostSerializer(serializers.ModelSerializer):
    comment_author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'blog',
            'updated_date',
            'created_date'
        )

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You have to log in')
        attrs['comment_author'] = request.user
        return attrs


class BlogListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    author = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    blog_comments = CommentListSerializer(many=True)

    class Meta:
        model = Blog
        fields = (
            'id',
            'blog_title',
            'blog_content',
            'blog_image',
            'category',
            'author',
            'comment_count',
            'blog_comments',
            'published_date'
        )

    def get_author(self, obj):
        if obj.author.get_full_name():
            return obj.author.get_full_name()
        return 'Admin User'
    
    def get_comment_count(self, obj):
        return obj.blog_comments.count()


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = (
            'id',
            'blog_title',
            'blog_content',
            'blog_image',
            'category',
            'author',
            'published_date'
        )

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You have to log in')
        attrs['author'] = request.user
        return attrs
