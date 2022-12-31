from django.contrib import admin

from multi_image.models import Student, StudentImage


class StudentImageInline(admin.StackedInline):
    model = StudentImage
    can_delete = False


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentImageInline,)
    list_display = ("name", "remarks")


# @admin.register(StudentImage)
# class StudentImageAdmin(admin.ModelAdmin):
#     list_display = ("id",)
