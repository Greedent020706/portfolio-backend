from django.contrib import admin
from django.utils.html import format_html

from .models import Project, Section, SiteProfile, Skill, Tag


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Solo puede existir una fila: si ya hay una, no se puede añadir otra.
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("nav_label", "kind", "slug", "order", "is_visible")
    list_editable = ("order", "is_visible")
    list_filter = ("kind", "is_visible")
    prepopulated_fields = {"slug": ("nav_label",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "order", "is_visible")
    list_display_links = ("title",)
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible", "tags")
    search_fields = ("title", "description")
    filter_horizontal = ("tags",)

    @admin.display(description="Imagen")
    def thumb(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" style="height:40px;border-radius:4px" alt="">',
            obj.image.url,
        )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("category", "order")


admin.site.register(Tag)

admin.site.site_header = "Panel del portfolio"
admin.site.site_title = "Portfolio"
admin.site.index_title = "Contenido"
