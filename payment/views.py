import braintree
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from .tasks import payment_completed
from orders.models import Order


gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # 获取nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # 创建和提交事务
        result = gateway.transaction.sale({
            'amount': f"{total_cost:.2f}",
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            # 启动异步任务发送邮件
            payment_completed.delay(order.id)
            return redirect('payment:done')

        else:
            return redirect('payment:canceled')

    else:
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       "client_token": client_token})


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_done(request):
    return render(request, 'payment/done.html')
