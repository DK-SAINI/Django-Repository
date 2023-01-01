from django.contrib import admin
from django.contrib.auth.models import User, Group

# from django.contrib.auth.admin import UserAdmin

from authentication.models import (
    UserProfile,
    EmailVerifyOtp,
    ForgotPasswordOtp,
)

from email_service.email import send_mail_to_service_partner


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("email", "first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("email",)
    inlines = (UserProfileInline,)

    # Customize Functions
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            send_mail_to_service_partner(obj)
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(EmailVerifyOtp)
admin.site.register(ForgotPasswordOtp)
