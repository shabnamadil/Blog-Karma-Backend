from django.urls import path

from .views import (
    BlogListCreateAPIView,
    BlogRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    CategoryListAPIView
)

urlpatterns = [
    path('blogs/', BlogListCreateAPIView.as_view(), name='blogs'),
    path('blogs/<str:slug>/', BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog-update-destroy'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-update-destroy'),
    path('categories/', CategoryListAPIView.as_view(), name='categories')
]

