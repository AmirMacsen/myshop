from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from shop.models import Product

from coupons.models import Coupon


class Order(models.Model):
    username = models.CharField(max_length=200, verbose_name="用户名")
    email = models.EmailField()
    address = models.CharField(max_length=200, verbose_name="地址")
    postal_code = models.CharField(max_length=20, verbose_name="邮政编码")
    city = models.CharField(max_length=100, verbose_name="城市")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    paid = models.BooleanField(default=False, verbose_name="支付")
    braintree_id = models.CharField(max_length=150, blank=True)

    coupon = models.ForeignKey(Coupon,
                               related_name="orders",
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "订单列表"

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal("100"))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="items",
                              on_delete=models.CASCADE,
                              verbose_name="订单")

    product = models.ForeignKey(Product,
                                related_name="order_items",
                                on_delete=models.CASCADE,
                                verbose_name="商品")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")

    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = "订单商品"
