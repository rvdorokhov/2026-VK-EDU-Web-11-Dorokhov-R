from django.contrib import admin

from core.models import User, Profile

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    class ProfileInline(admin.TabularInline):
        model = Profile

        fields = (
            "nickname",
            "avatar",
        )

        extra = 0

    inlines = (ProfileInline,)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nickname",
        "avatar",

        "user__id",
        "user__email",
    )

    list_select_related = (
        "user",
    )

    raw_id_fields = (
        "user",
    )

    search_fields = (
        "user__id",
        "user__email",

        "nickname",
    )