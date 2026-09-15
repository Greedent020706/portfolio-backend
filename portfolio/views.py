from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Section, SiteProfile
from .serializers import SectionSerializer, SiteProfileSerializer


@method_decorator(cache_page(60), name="dispatch")
class SiteView(APIView):
    """Devuelve todo el contenido del portfolio en una sola respuesta."""

    def get(self, request):
        profile = SiteProfile.objects.first()
        sections = Section.objects.filter(is_visible=True)

        return Response({
            "profile": SiteProfileSerializer(
                profile, context={"request": request}
            ).data if profile else None,
            "sections": SectionSerializer(
                sections, many=True, context={"request": request}
            ).data,
        })
