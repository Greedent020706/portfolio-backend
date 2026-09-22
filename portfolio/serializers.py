from rest_framework import serializers

from .models import Project, Section, SiteProfile, Skill


class SiteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = ["name", "role", "summary", "email", "avatar"]


class ProjectSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Project
        fields = ["id", "title", "description", "image", "url", "repo_url", "tags"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "icon"]


class SectionSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["slug", "kind", "nav_label", "heading", "body", "image", "content"]

    def get_content(self, section):
        """Cada tipo de sección trae los datos que le corresponden."""
        if section.kind == Section.Kind.PROJECTS:
            projects = Project.objects.filter(is_visible=True).prefetch_related("tags")
            return {"projects": ProjectSerializer(
                projects, many=True, context=self.context
            ).data}

        if section.kind == Section.Kind.SKILLS:
            return {"skills": SkillSerializer(
                Skill.objects.all(), many=True, context=self.context
            ).data}

        return {}