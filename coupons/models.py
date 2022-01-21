from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="优惠券码")
    valid_from = models.DateTimeField(verbose_name="开始时间")
    valid_to = models.DateTimeField(verbose_name="结束时间")

    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="折扣"
    )

    active = models.BooleanField(verbose_name="使用")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "优惠券"