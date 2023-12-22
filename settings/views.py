from django.shortcuts import render, HttpResponse
from django.core import serializers
from settings.models import District,Plan
# import razorpay


# Create your views here.


def getdistictbystateid(request, pk):
    try:
        __Data = District.objects.filter(state_id=pk)
        qs_json = serializers.serialize('json', __Data)
        return HttpResponse(qs_json, content_type='application/json')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex, content_type='application/json')


def getdetailsbyplan(request, pk):
    try:
        __Data = Plan.objects.filter(id=pk)
        qs_json = serializers.serialize('json', __Data)
        return HttpResponse(qs_json, content_type='application/json')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex, content_type='application/json')


def getOrderID(request, amt):
    __context = {}
    import json
    try:        
        __context['order_Key'] = 'rzp_live_SAQqLTl1SzdQZ6'
        razorpay_client = razorpay.Client(
            auth =('rzp_live_SAQqLTl1SzdQZ6','ALm7v3J3m1D5avK3jY4OgZy6')
        )

        order = razorpay_client.order.create(dict(amount=amt, currency='INR',
                                                    receipt = '',notes = {},payment_capture ='1'))
        order['order_Key']='rzp_live_SAQqLTl1SzdQZ6'

        return HttpResponse(json.dumps(order), content_type='application/json')

    except Exception as error:
        print(error)
        return render(request, 'error.html', {'error': error})
