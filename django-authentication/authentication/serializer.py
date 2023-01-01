from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import UserProfile, EmailVerifyOtp


class UserProfileSerializer(serializers.Serializer):
    job_title = serializers.CharField(required=False)
    telephone_no = serializers.CharField(required=False)
    company_name = serializers.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = (
            "job_title",
            "company_name",
            "telephone_no",
            "address_line_one",
            "address_line_two",
            "country",
            "city",
            "photo",
        )


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=("Username already exists"),
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message=("email already exists"),
            )
        ],
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        # These are the fields that our registration form is contains.
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "profile",
        )
        # We can add extra validations with extra_kwargs option
        # We set first_name and last_name required.
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        # Password fields must be same. We can validate these fields with serializers validate() method
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs


class SendOtpEmailVerifySerialize(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]


class EmailVerifySerialize(serializers.Serializer):
    otp = serializers.CharField(required=True)

    class Meta:
        model = EmailVerifyOtp
        fields = ["otp"]


class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, attrs):
        # Password fields must be same.
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]


class ConfirmForgotPasswordSerializer(serializers.Serializer):
    otp = serializers.IntegerField(allow_null=False, required=True)
    password = serializers.CharField(
        allow_null=False,
        required=True,
        min_length=8,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["otp", "password"]


class UserDetailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    profile = UserProfileSerializer()

    class Meta:
        Model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        # Profile Update
        instance.profile.company_name = validated_data["profile"][
            "company_name"
        ]
        # save Profile data
        instance.profile.save()
        # save User data
        instance.save()
        return instance
