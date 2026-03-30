from django.urls import path
from . import views

urlpatterns = [
    # SPA
    path('', views.index, name='index'),

    # Auth
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/auth/me/', views.api_me, name='api_me'),

    # Restaurants
    path('api/restaurants/', views.api_restaurants, name='api_restaurants'),
    path('api/restaurants/<int:pk>/', views.api_restaurant_detail, name='api_restaurant_detail'),

    # Orders
    path('api/orders/place/', views.api_place_order, name='api_place_order'),
    path('api/orders/history/', views.api_order_history, name='api_order_history'),

    # Favourites
    path('api/favourites/', views.api_favourites, name='api_favourites'),
    path('api/favourites/toggle/', views.api_toggle_favourite, name='api_toggle_favourite'),

    # Address
    path('api/address/update/', views.api_update_address, name='api_update_address'),

    # Promo
    path('api/promo/apply/', views.api_apply_promo, name='api_apply_promo'),

    # Search
    path('api/search/', views.api_search, name='api_search'),

    # Admin
    path('api/admin/stats/', views.api_admin_stats, name='api_admin_stats'),
]
