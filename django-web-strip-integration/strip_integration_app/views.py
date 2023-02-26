from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView


# Strip
import stripe

# get stripe secret key
stripe.api_key = settings.STRIPE_SK


def home(request):
    try:
        # Get product list from strip portal
        plan_list = stripe.Product.list(limit=3).data
        return render(request, 'home.html', context={'plan_list': plan_list})
    except Exception:
        return render(request, 'home.html', context={'error': 'No Internet Connection'})


def checkout_Session_create(request, id):

    product = stripe.Product.retrieve(id)

    checkout_session = stripe.checkout.Session.create(
        # Return on success page after payment done
        success_url="http://127.0.0.1:8000/success",
        # Return on cancel page.
        cancel_url="http://127.0.0.1:8000/cancel",
        # Payment method
        payment_method_types=['card'],
        line_items=[
            {
                "price": product.default_price,
                "quantity": 1,
            },
        ],
        # mode subscription, payment
        mode="subscription",
    )
    # redirect on url
    return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"
