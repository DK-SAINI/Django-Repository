from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=14)
    telephone_no = models.CharField(max_length=14)
    address_line_one = models.CharField(max_length=255)
    address_line_two = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="uploads", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"


class EmailVerifyOtp(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, blank=False
    )
    otp = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "email_verify_otp"


class ForgotPasswordOtp(models.Model):
    class Meta:
        db_table = "forgot_password_otp"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, blank=False
    )
    otp = models.IntegerField(null=False, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
