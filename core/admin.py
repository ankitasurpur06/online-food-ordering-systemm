from django.contrib import admin
from .models import (
    Restaurant, MenuItem, Order, OrderItem, Cuisine,
    UserProfile, Address, PromoCode, Favourite, Review
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'rating', 'is_open', 'is_featured', 'total_orders')
    list_filter = ('is_open', 'is_featured', 'is_veg', 'city')
    search_fields = ('name', 'address')
    filter_horizontal = ('cuisines',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_veg', 'is_available', 'is_bestseller')
    list_filter = ('category', 'is_veg', 'is_available', 'is_bestseller')
    search_fields = ('name', 'restaurant__name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'restaurant__name')
    inlines = [OrderItemInline]
    readonly_fields = ('subtotal', 'delivery_fee', 'taxes', 'total')


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name', 'kitchen_count')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_admin')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'discount_flat', 'used_count', 'is_active')


admin.site.register(Address)
admin.site.register(Favourite)
admin.site.register(Review)
