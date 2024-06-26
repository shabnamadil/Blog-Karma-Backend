from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)

from apps.core.models import (
    ContactInformation,
    ContactMessage, 
    AboutUs
)
from .serializers import (
    ContactInformationSerializer,
    ContactMessagePostSerializer,
    AboutUsInformationSerializer
)


class ContactInformationGetAPIView(ListAPIView):
    serializer_class = ContactInformationSerializer
    queryset = ContactInformation.objects.all()


class ContactMessagePostAPIView(CreateAPIView):
    serializer_class = ContactMessagePostSerializer
    queryset = ContactMessage.objects.all()


class AboutUsGetAPIView(ListAPIView):
    serializer_class = AboutUsInformationSerializer
    queryset = AboutUs.objects.all()

