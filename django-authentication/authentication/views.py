from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout

# Import Rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# import model
from authentication.models import (
    UserProfile,
    EmailVerifyOtp,
    ForgotPasswordOtp,
)

# importr serializer
from authentication.serializer import (
    UserRegisterSerializer,
    SendOtpEmailVerifySerialize,
    EmailVerifySerialize,
    UserLogInSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ConfirmForgotPasswordSerializer,
    UserDetailSerializer,
)

from email_service.email import send_mail_for_verify_email

import random
import string


class UserRegistrationView(APIView):
    def post(self, request):
        serializer_class = UserRegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            profile_data = request.data.pop("profile")
            password = request.data.pop("password")
            request.data.pop("password2")
            user = User(**request.data)
            user.set_password(password)
            user.is_active = False
            user.save()

            # ADD GROUP
            group = Group.objects.get(name="customer")
            user.groups.add(group)

            # ADD USER PROFILE DATA
            UserProfile.objects.create(user=user, **profile_data)

            # GENRATE OTP FOR REGISTER USER
            otp = "".join(random.choices(string.digits, k=4))
            otp_obj = EmailVerifyOtp.objects.create(user=user, otp=otp)

            # SEND OTP ON REGISTER EMIAL
            send_mail_for_verify_email(otp_obj)

            response = {"message": "user registered successfully."}
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer_class.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class SendOtpEmailVerifyView(APIView):
    def post(self, request):
        serializer_class = SendOtpEmailVerifySerialize(data=request.data)
        if serializer_class.is_valid():
            email = request.data.get("email")
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                # DELETE OLD OTP
                EmailVerifyOtp.objects.filter(user=user).delete()

                # GENRATE OTP FOR REGISTER USER
                otp = "".join(random.choices(string.digits, k=4))
                otp_obj = EmailVerifyOtp.objects.create(user=user, otp=otp)

                # SEND OTP ON REGISTER EMIAL
                send_mail_for_verify_email(otp_obj)
                return Response(
                    data={"message": "OTP is sent to the registered email"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"message": "email not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class EmailVerifyView(APIView):
    def post(self, request):
        serializer_class = EmailVerifySerialize(data=request.data)
        if serializer_class.is_valid():
            otp = request.data.get("otp")
            # CHECK OTP EXIST OR NOT
            if EmailVerifyOtp.objects.filter(otp=otp).exists():
                user_otp = EmailVerifyOtp.objects.get(otp=otp)
                User.objects.filter(id=user_otp.user.id).update(is_active=True)
                EmailVerifyOtp.objects.filter(otp=otp).delete()
                return Response(
                    data={"message": "Email verification successfully done."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"message": "Enter otp is wrong."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogInView(APIView):
    def post(self, request):
        data = {}
        serializer_class = UserLogInSerializer(data=request.data)
        if serializer_class.is_valid():
            username = serializer_class.validated_data["username"]
            password = serializer_class.validated_data["password"]

            user = User.objects.filter(username=username).exists()

            if user is False:
                response = {"message": "Incorrect username"}
                return Response(
                    data=response, status=status.HTTP_400_BAD_REQUEST
                )

            user_account = User.objects.get(username=username)
            token = Token.objects.get_or_create(user=user_account)[0].key
            if not check_password(password, user_account.password):
                response = {"message": "Incorrect Login credentials"}
                return Response(
                    data=response, status=status.HTTP_400_BAD_REQUEST
                )

            if user_account.is_active:
                login(request, user_account)
                data["message"] = "user logged in"
                data["username"] = user_account.username

                response = {
                    "data": data,
                    "token": token,
                }

                return Response(response, status=status.HTTP_200_OK,)

            else:
                return Response(
                    data={"message": "Account not active"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogOutView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)

        return Response(
            data={"message": "User Logged out successfully"},
            status=status.HTTP_200_OK,
        )


class UserChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer_class = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer_class.is_valid():
            # Set New Password & Save it
            self.request.user.set_password(request.data.get("new_password"))
            self.request.user.save()
            response = {"message": "Password updated successfully"}
            return Response(response, status=status.HTTP_200_OK)

        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer_class = ForgotPasswordSerializer(data=request.data)
        if serializer_class.is_valid():
            email = request.data.get("email")
            user_exist = User.objects.filter(email=email).exists()
            if user_exist is False:
                return Response(
                    data={"message": "Incorrect Email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(email=request.data.get("email"))
            # Remove Old Otp
            ForgotPasswordOtp.objects.filter(user=user).delete()

            # GENRATE OTP FOR REGISTER USER
            otp = "".join(random.choices(string.digits, k=4))
            otp_obj = ForgotPasswordOtp.objects.create(user=user, otp=otp)

            # SEND OTP ON REGISTER EMIAL
            send_mail_for_verify_email(otp_obj)
            return Response(
                data={"message": "Check otp on your email"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class ConfirmForgotPasswordView(APIView):
    def post(self, request):
        serializer_class = ConfirmForgotPasswordSerializer(data=request.data)
        if serializer_class.is_valid():
            otp = request.data.get("otp")
            check_otp = ForgotPasswordOtp.objects.filter(otp=otp).exists()
            if check_otp is False:
                return Response(
                    data={"message": "Incorrect OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = ForgotPasswordOtp.objects.get(otp=otp).user
            user.set_password(request.data.get("password"))
            user.save()
            # Remove OTP
            ForgotPasswordOtp.objects.filter(otp=otp).delete()
            return Response(
                data={"message": "New Password set successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # 3. Retrieve
    def get(self, request):
        user_obj = User.objects.get(id=request.user.id)
        serializer = UserDetailSerializer(user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(sef, request, *args, **kwargs):
        user_obj = User.objects.get(id=request.user.id)
        serializer_class = UserDetailSerializer(
            instance=user_obj, data=request.data, partial=True
        )
        if serializer_class.is_valid():
            serializer_class.save()
            data = {
                "message": "Record updated successfully",
                "data": [serializer_class.data],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            data=serializer_class.errors, status=status.HTTP_400_BAD_REQUEST,
        )
