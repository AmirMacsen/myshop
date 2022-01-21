import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def export_to_csv(modeladmin: admin.ModelAdmin, request, queryset):
    opts = modeladmin.model._meta

    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    # 解决中文乱码
    response.charset = 'utf-8-sig'
    response['Content-Disposition'] = content_disposition
    # 向response中写入csv
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y/%m/%d')

            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = "导出为CSV"


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">详情</a>')


def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">pdf</a>')


order_pdf.short_description = "生成发票"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    row_id_field = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated',
                    order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    # 注册事件
    actions = [export_to_csv]
