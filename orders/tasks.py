from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order_id}"
    message = f"您好，{order.username},、\n\n " \
              f"您于{order.created}成功提交了一个订单。" \
              f"订单ID为{order.id}"

    mail_sent = send_mail(subject,
                          message,
                          '3254168608@qq.com',
                          [order.email, ])

    return mail_sent
