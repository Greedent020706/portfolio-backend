from django.db import models
from django.core.validators import FileExtensionValidator


class SiteProfile(models.Model):
    """Datos generales del sitio. Solo existe una fila."""
    name = models.CharField("Nombre", max_length=80)
    role = models.CharField("Rol", max_length=120)
    summary = models.TextField("Resumen", blank=True)
    email = models.EmailField("Correo", blank=True)
    avatar = models.ImageField("Foto", upload_to="profile/", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil del sitio"
        verbose_name_plural = "Perfil del sitio"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Fuerza que siempre sea la misma fila: patrón singleton.
        self.pk = 1
        super().save(*args, **kwargs)


class Section(models.Model):
    class Kind(models.TextChoices):
        HERO = "hero", "Portada"
        TEXT = "text", "Texto"
        SKILLS = "skills", "Stack tecnológico"
        PROJECTS = "projects", "Proyectos"
        CONTACT = "contact", "Contacto"

    slug = models.SlugField(
        "Identificador", unique=True,
        help_text="Se usa en la URL. Ej: 'proyectos' produce #proyectos",
    )
    kind = models.CharField("Tipo", max_length=20, choices=Kind.choices)
    nav_label = models.CharField("Etiqueta del menú", max_length=40)
    heading = models.CharField("Título", max_length=120, blank=True)
    body = models.TextField("Texto", blank=True)
    image = models.ImageField("Imagen", upload_to="sections/", blank=True, null=True)
    order = models.PositiveIntegerField("Orden", default=0, db_index=True)
    is_visible = models.BooleanField("Visible", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"

    def __str__(self):
        return f"{self.order}. {self.nav_label}"


class Tag(models.Model):
    name = models.CharField("Nombre", max_length=40, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField("Título", max_length=120)
    description = models.TextField("Descripción")
    image = models.ImageField("Imagen", upload_to="projects/", blank=True, null=True)
    url = models.URLField("Enlace", blank=True)
    repo_url = models.URLField("Repositorio", blank=True)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")
    order = models.PositiveIntegerField("Orden", default=0, db_index=True)
    is_visible = models.BooleanField("Visible", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField("Nombre", max_length=60)
    category = models.CharField("Categoría", max_length=60, blank=True)
    icon = models.FileField(
        "Icono",
        upload_to="skills/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["svg", "png", "webp", "jpg", "jpeg"])],
        help_text="SVG o PNG cuadrado. Recomendado: SVG.",
    )
    order = models.PositiveIntegerField("Orden", default=0, db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Tecnología"
        verbose_name_plural = "Tecnologías"

    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name = models.CharField("Nombre", max_length=100)
    email = models.EmailField("Correo")
    message = models.TextField("Mensaje")
    ip = models.GenericIPAddressField("IP", blank=True, null=True)
    created_at = models.DateTimeField("Recibido", auto_now_add=True)
    is_read = models.BooleanField("Leído", default=False)
    email_sent = models.BooleanField("Correo enviado", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return f"{self.name} <{self.email}>"