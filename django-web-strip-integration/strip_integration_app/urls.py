from django.urls import path

from strip_integration_app import views
from strip_integration_app.views import CancelView, SuccessView

urlpatterns = [
    path('', views.home, name="home"),
    path('checkout_Session_create/<id>', views.checkout_Session_create, name="checkout"),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
