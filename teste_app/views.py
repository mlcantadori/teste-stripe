from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
import logging
import stripe

# Create your views here.
def checkout_view(request):

    amount = 1000
    intent = stripe.PaymentIntent.create(
         amount=amount,
         currency='usd',
         # Verify your integration in this guide by including this parameter
         metadata={'integration_check': 'accept_a_payment'},
    )

    stripe_dict={'stripe_publishable_key':settings.STRIPE_PUBLISHABLE_API_KEY,'client_secret':intent.client_secret,'amount':amount}
    return render(request,'teste_app/checkout.html',context=stripe_dict)

# @csrf_exempt
# @require_POST
# def webhook(request):
#     print('oi')
#     jsondata = request.body
#     data = json.loads(jsondata)
#     print(data['type'])
#     if data['type'] == 'payment_intent.succeeded':
#         logger = logging.getLogger('stripe_log')
#         logger.info(data)
#
#     return HttpResponse(status=200)

@require_POST
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
        logger = logging.getLogger('stripe_log')
        logger.info(json.loads(payload))
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
        # ... handle other event types
    else:
        # Unexpected event type
        return HttpResponse(status=200)

    return HttpResponse(status=200)
