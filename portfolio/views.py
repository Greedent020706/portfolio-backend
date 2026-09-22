import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import ContactMessage, Section, SiteProfile
from .serializers import ContactSerializer, SectionSerializer, SiteProfileSerializer

logger = logging.getLogger(__name__)


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

def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class ContactView(APIView):
    """Recibe el formulario de contacto: guarda el mensaje y avisa por correo."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Bot detectado: respondemos "ok" para no darle pistas, pero no guardamos.
        if data.get("website"):
            return Response(status=201)

        msg = ContactMessage.objects.create(
            name=data["name"],
            email=data["email"],
            message=data["message"],
            ip=client_ip(request),
        )

        safe_name = msg.name.replace("\r", " ").replace("\n", " ")
        try:
            EmailMessage(
                subject=f"[Portfolio] Mensaje de {safe_name}",
                body=f"De: {msg.name} <{msg.email}>\n\n{msg.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECIPIENT],
                reply_to=[msg.email],
            ).send()
            msg.email_sent = True
            msg.save(update_fields=["email_sent"])
        except Exception:
            # El mensaje ya está guardado; el fallo de correo no debe romper la respuesta.
            logger.exception("No se pudo enviar el correo de contacto")

        return Response(status=201)