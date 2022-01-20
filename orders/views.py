from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            # 发送异步任务
            order_created.delay(order.id)

            # 支付
            request.session['order_id'] = order.id

            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    return render(request,
                  "orders/order/create.html",
                  {"cart": cart,
                   "form": form})
