from django.urls import path

from multi_image.views import StudentView

urlpatterns = [
    path(
        "create_student_with_multi_image/",
        StudentView.as_view(),
        name="create_student_with_multi_image",
    ),
]
