from django.urls import path

from .views import (
    BlogListCreateAPIView,
    CommentListCreateAPIView
)

urlpatterns = [
    path('blogs/', BlogListCreateAPIView.as_view(), name='blogs'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comments')
]

