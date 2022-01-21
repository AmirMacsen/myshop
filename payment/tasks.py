from io import BytesIO
from celery import task
import weasyprint
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from orders.models import Order


@task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)

    # email
    subject = f"My Shop商城发票  订单编号：{order.id}"
    message = '请您查收附件中的发票'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])

    # 生成PDF
    html = render_to_string("orders/order/pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # 添加附件
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    email.send()
