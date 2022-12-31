from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    remarks = models.TextField()


class StudentImage(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField(upload_to="", blank=True, null=True)
