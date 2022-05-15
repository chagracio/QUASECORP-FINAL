from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from c3gUsers.decorators import allowed_users
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.models import User
from django.db.models import F
from django.core.exceptions import *
from django.http import HttpResponse

#==================INDEX============================
def index (request):
    return render(request, 'index.html')

#==================ADMIN DASHBOARD============================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard (request):
    rice_list = RiceItem.objects.all()
    return render(request, 'AdminFolder/index.html', {'rice_list':rice_list})

#==================RICE LIST============================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def RiceList(request):
    rice_list = RiceItem.objects.all()
    return render(request, 'AdminFolder/RiceList.html', {'rice_list':rice_list})

#==================ADDING RICE============================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addRice (request):
    rice_form = RiceItemForm()
    if request.method == 'POST':
        rice_form = RiceItemForm(request.POST, request.FILES)
        if rice_form.is_valid():
            rice_form.save()
        messages.success(request, "Rice Item has been successfully added!")
        return redirect('ricelist')
    return render(request, 'AdminFolder/AddRice.html', {'rice_form':rice_form})

#==================DELETE RICE============================
def deleteRice(request, id):
    rice = RiceItem.objects.get(id=id)
    rice.delete()
    return redirect('ricelist')

#==================UPDATE RICE============================
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateRice(request, id):
    rice = RiceItem.objects.get(id=id)
    rice_form = RiceItemForm(instance=rice)
    if request.method == 'POST':
        rice_form = RiceItemForm(request.POST, instance=rice)
        if rice_form.is_valid():
            rice_form.save()
        messages.success(request, "Rice Item has been updated!")
        return redirect('ricelist')
    return render(request, 'AdminFolder/UpdateRiceItem.html', {'rice_form':rice_form})

#==================CUSTOMER HOMEPAGE============================
@login_required(login_url='login')
def CustomerHomepage(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    riceitems = order.orderriceitems_set.all()

    rice_item = RiceItem.objects.all()
    context = {
        'rice_item':rice_item,
        'riceitems':riceitems,
        'order':order}
    return render(request, 'Customer.html', context)

#==================CHECK OUT============================
@login_required(login_url='login')
def Checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    riceitems = order.orderriceitems_set.all()

    rice_item = RiceItem.objects.all()
    context = {
        'rice_item':rice_item,
        'riceitems':riceitems,
        'order':order,
        'customer':customer,
        }
    return render(request, 'PlaceorderPage.html', context)

#==================UPDATE CART ITEMS============================
@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    rice = RiceItem.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderRiceitem, created = OrderRiceItems.objects.get_or_create(order=order, rice=rice)
    
    if action == 'add':
        orderRiceitem.quantity = (orderRiceitem.quantity + 1)
    elif action == 'remove':
        orderRiceitem.quantity = (orderRiceitem.quantity - 1)

    orderRiceitem.save()

    if action == 'del':
        orderRiceitem.delete()

    # if orderRiceitem.quantity <= 0:
    #     orderRiceitem.delete()
    
    return JsonResponse('Item was added', safe=False)

#==================PROCESSING ORDER============================
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data =  json.loads(request.body)
    
    customer = request.user.customer

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # riceitems = order.orderriceitems_set.all()

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True      
    order.save()

    OrderDetails.rice_ordered = OrderRiceItems.objects.all()

    OrderDetails.objects.create(
        customer=customer,
        order=order,
        # rice_ordered = OrderDetails.rice_ordered,
        total_payment=total,
        address=data['form']['address'],
        ContactNum=data['form']['tel'],
        shippingMeth=data['form']['shippingMeth'],
        shippingStatus='Order Submitted',
        orderStatus='Owner is Validating your order',
    )

    return JsonResponse('Order Submitted', safe=False)

#==================ORDER STATUS(customer side)============================
def CustomerDashboard(request):
    customer = request.user.customer
    orderdetails = OrderDetails.objects.filter(customer = customer)

    context = {

        'orderdetails':orderdetails,
        }
    return render(request, 'CustomerDashboard.html', context)

#==================INQUIRY/CONTACT US============================
def Inquiry(request):
    return render(request, 'Inquiry.html')

#==================LENDING STATUS(customer side)============================
def LendingStatus(request):
    customer = request.user.customer
    orderdetails = OrderDetails.objects.filter(customer = customer)
    lendingstat = LendingStat.objects.filter(customer = customer)
    
    context = {
        'lendingstat':lendingstat,
        'orderdetails':orderdetails
    }
    return render(request, 'LendingStatus.html', context)

#==================ADMIN ACCESS TO LIST OF ORDERS============================
def orders(request):

    orderdetails = OrderDetails.objects.all()
    context = {
        'orderdetails':orderdetails,
        }
    return render(request, 'AdminFolder/ListOfOrders.html', context)


#==================ADMIN TO UPDATE CUSTOMER ORDER STATUS============================
def UpdateOrderStatus(request, id):
    orderdeets = OrderDetails.objects.get(id=id)
    orderform = CustomerOrderForm(instance=orderdeets)
    if request.method == 'POST':
        orderform = CustomerOrderForm(request.POST, instance=orderdeets)
        if orderform.is_valid():
            orderform.save()
        return redirect('orders')

    orderdetails = OrderDetails.objects.get(id=id)

    if orderdeets.orderStatus == 'Accepted':
        LendingStat.objects.create(
            customer=orderdetails.customer,
            ContactNum=orderdetails.ContactNum,
            total_payment=orderdetails.total_payment,
            amount_paid=0,
            balance=orderdetails.total_payment,
            status='Unpaid',
            date_added = models.DateTimeField(auto_now_add = True)
        )
    context = {
        'orderdetails':orderdetails,
        'orderform':orderform
    }
    return render(request, 'AdminFolder/UpdateOrderStatus.html', context)

#==================ADMIN ACCESS TO CUSTOMER LENDING STATUS============================
def CustomerStatus(request):
    lendingDeets = LendingStat.objects.all()
    return render(request, 'AdminFolder/lendingStat.html', {'lendingDeets':lendingDeets})

def UpdateLendingStatus(request, id):
    lendingDeets = LendingStat.objects.get(id=id)
    lending_form = LendingForm(instance=lendingDeets)
    if request.method == 'POST':
        lending_form = LendingForm(request.POST, instance=lendingDeets)
        if lending_form.is_valid():
            lending_form.save()
            
            lendingDeets.balance = F('total_payment') - F('amount_paid')

            if lendingDeets.balance == 0:
                lendingDeets.status = 'Paid'
            
            lendingDeets.save()

        return redirect('customerLendingStatus')

    context = {
        'lending_form':lending_form
    }
    return render(request, 'AdminFolder/UpdateLendingStatus.html', context)