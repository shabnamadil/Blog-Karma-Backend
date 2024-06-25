from rest_framework.generics import (
    ListCreateAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.blogs.models import (
    Blog,
    Comment
)
from .serializers import (
    BlogListSerializer,
    BlogPostSerializer,
    CommentListSerializer,
    CommentPostSerializer
)


class BlogListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogListSerializer
    queryset = Blog.published.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = BlogPostSerializer
        return super().get_serializer_class()
    

class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.published.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = CommentPostSerializer
        return super().get_serializer_class()
