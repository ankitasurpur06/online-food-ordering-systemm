from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    avatar_initial = models.CharField(max_length=2, default='U')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"


class Address(models.Model):
    ADDRESS_TYPES = [('home', 'Home'), ('work', 'Work'), ('other', 'Other')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='home')
    full_address = models.TextField()
    city = models.CharField(max_length=100, default='Kalaburagi')
    pincode = models.CharField(max_length=10, default='585101')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.label}"


class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    kitchen_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Kalaburagi')
    image_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    delivery_time_min = models.IntegerField(default=25)
    delivery_time_max = models.IntegerField(default=35)
    delivery_fee = models.IntegerField(default=0)  # 0 = free
    min_order = models.IntegerField(default=100)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    is_veg = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    has_offer = models.BooleanField(default=False)
    offer_text = models.CharField(max_length=100, blank=True)
    badge = models.CharField(max_length=50, blank=True)  # e.g., "TOP RATED", "NEW"
    total_orders = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def delivery_time_display(self):
        return f"{self.delivery_time_min}-{self.delivery_time_max} min"

    @property
    def delivery_fee_display(self):
        return "FREE" if self.delivery_fee == 0 else f"₹{self.delivery_fee}"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starters'),
        ('main', 'Main Course'),
        ('breads', 'Breads & Rice'),
        ('dessert', 'Desserts'),
        ('drinks', 'Drinks'),
        ('sides', 'Sides'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    image_url = models.URLField(blank=True)
    is_veg = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    spice_level = models.IntegerField(default=0, choices=[(0, 'Mild'), (1, 'Medium'), (2, 'Spicy'), (3, 'Extra Spicy')])
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    delivery_address = models.TextField()
    subtotal = models.IntegerField(default=0)
    delivery_fee = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    special_instructions = models.TextField(blank=True)
    courier_name = models.CharField(max_length=100, default='Marcus Chen')
    estimated_delivery_minutes = models.IntegerField(default=35)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update restaurant stats
        if self.status == 'delivered':
            Restaurant.objects.filter(pk=self.restaurant_id).update(
                total_orders=models.F('total_orders') + 1,
                revenue=models.F('revenue') + self.total
            )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # snapshot
    price = models.IntegerField()              # snapshot
    quantity = models.IntegerField(default=1)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.name}"


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    discount_percent = models.IntegerField(default=0)
    discount_flat = models.IntegerField(default=0)
    min_order = models.IntegerField(default=0)
    max_uses = models.IntegerField(default=1000)
    used_count = models.IntegerField(default=0)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.restaurant.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username} → {self.restaurant.name} ({self.rating}★)"
