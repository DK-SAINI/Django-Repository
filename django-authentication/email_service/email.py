from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_mail_for_verify_email(otp_obj):
    subject = "OTP"
    data = {"user": otp_obj.user, "otp": otp_obj.otp}
    message = get_template("otp.html").render(data)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[otp_obj.user.email],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()


def send_mail_to_service_partner(obj):
    subject = "Partner Account Detail"
    message = """
        <p>
            <span>UserName:""" + obj.username + """</span><br/>
            <span>Password:""" + obj.password + """</span><br/>
            <span>Email:""" + obj.email + """</span><br/>
        </p>
    """
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[obj.email],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()
