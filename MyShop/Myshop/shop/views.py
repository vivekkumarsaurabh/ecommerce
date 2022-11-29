from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
#from PayTm import Checksum.py

MERCHANT_KEY = 'WorldP64425807474247'

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)

    # params = {'no_of_slides':nslides,'range':range(1,nslides), 'product': products}
    allprods = []
    catprods = Product.objects.values('categories', 'id')
    cats = {item['categories'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(categories=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])

    # allprods = [[products,range(1, nslides),nslides],
    # [products,range(1,nslides),nslides]]
    params = {'allprods': allprods}
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    thank=False
    if request.method == 'POST':
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        mobile = request.POST.get('mobile', '')
        desc = request.POST.get('desc', '')

        print(name, email, mobile, address, desc)
        contact = Contact(name=name, email=email, mobile=mobile, address=address, desc=desc)
        contact.save()
        thank=True

    return render(request, "shop/contact.html", {'thank':thank})


def search(request):
    return render(request, "shop/search.html")

'''
def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.Objects.filter(orderId=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.Objects.filter(orderId=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dump(updates, default=str)
                return HttpResponse(response)

            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, "shop/tracker.html")



'''
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_Json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, "shop/tracker.html")

def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodview.html", {'product': product[0]})


def checkout(request):
    if request.method == 'POST':
        print(request)
        item_Json = request.POST.get('item_Json', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        address_2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        mobile = request.POST.get('mobile', '')

        print(item_Json, name, email, address, address_2, city, state, zip_code, mobile)
        order = Orders(item_Json=item_Json, name=name, email=email, address=address, address_2=address_2, city=city, state=state,
                       zip_code=zip_code, mobile=mobile, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id= order.order_id
        return render(request, "shop/checkout.html", {'thank':thank, 'id':id})
        #request paytm to transfer the amount to your account after payment by user
        '''param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': 'order.order_id',
            'TXN_AMOUNT': '1',
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)'''
        #return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, "shop/checkout.html")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
