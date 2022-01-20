from django.urls import reverse

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name="商品分类")
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "category"
        verbose_name_plural = "商品分类"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products",
                                 on_delete=models.CASCADE)

    name = models.CharField(max_length=200, db_index=True, verbose_name="商品名称")
    slug = models.SlugField(max_length=200, db_index=True, )
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True,
                              verbose_name="图片")
    description = models.TextField(blank=True, verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    available = models.BooleanField(default=True, verbose_name="是否有库存")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name_plural = "商品列表"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
