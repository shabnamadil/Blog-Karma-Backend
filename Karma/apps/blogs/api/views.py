from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from apps.blogs.models import (
    Blog,
    Comment,
    Category
)
from .serializers import (
    BlogListSerializer,
    BlogPostSerializer,
    CommentListSerializer,
    CommentPostSerializer,
    CategoryListSerializer
)


class BlogListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogListSerializer
    queryset = Blog.published.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = BlogPostSerializer
        return super().get_serializer_class()
    

class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogListSerializer
    queryset = Blog.published.all()
    permission_classes = (IsAuthenticated,)
    

class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.published.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = CommentPostSerializer
        return super().get_serializer_class()
    

class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.published.all()
    permission_classes = IsAuthenticated
    

class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()