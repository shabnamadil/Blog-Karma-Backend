from django.urls import path

from .views import (
    ContactInformationGetAPIView,
    ContactMessagePostAPIView,
    AboutUsGetAPIView
)

urlpatterns = [
    path('contact/', ContactInformationGetAPIView.as_view(), name='contact'),
    path('message/', ContactMessagePostAPIView.as_view(), name='message'),
    path('about/', AboutUsGetAPIView.as_view(), name='about-us')
]