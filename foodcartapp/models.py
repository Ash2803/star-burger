from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'title',
        max_length=50
    )
    address = models.CharField(
        'address',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'contact telephone',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'title',
        max_length=50
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'title',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='category',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'price',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'image'
    )
    special_status = models.BooleanField(
        'special offer',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'description',
        max_length=255,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="restaurant",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='product',
    )
    availability = models.BooleanField(
        'for sale',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Menu item of a restaurant'
        verbose_name_plural = 'Menu items of a restaurant'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    client_name = models.CharField('Client name', max_length=100, db_index=True)
    client_number = PhoneNumberField()
    products = models.ManyToManyField(
        Product,
        through='OrderProduct',
        related_name='orders',
    )
    delivery_address = models.CharField(
        'address',
        max_length=100,
    )
    created_at = models.DateTimeField('Order date', auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.client_name


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='order',
        related_name='order_products',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='product',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])

    class Meta:
        verbose_name = 'Order product'
        verbose_name_plural = 'Order products'

    def __str__(self):
        return f"{self.order} - {self.product}"
