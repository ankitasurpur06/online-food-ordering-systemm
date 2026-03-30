import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import (
    Restaurant, MenuItem, Order, OrderItem,
    UserProfile, Address, Cuisine, PromoCode, Favourite
)


# ─── MAIN SPA VIEW ─────────────────────────────────────────────────────────────

def index(request):
    """Serve the main Single-Page Application."""
    user_data = None
    if request.user.is_authenticated:
        user_data = {
            'id': request.user.id,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'is_admin': request.user.email == 'admin@quickbite.com',
            'initial': (request.user.get_full_name() or request.user.username)[0].upper(),
        }
        user_data = json.dumps(user_data)
    return render(request, 'core/index.html', {'user_data': user_data})


# ─── AUTH API ──────────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def api_login(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    try:
        user_obj = User.objects.get(email=email)
        user = authenticate(request, username=user_obj.username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.get_full_name() or user.username,
                    'email': user.email,
                    'is_admin': user.email == 'admin@quickbite.com',
                    'initial': (user.get_full_name() or user.username)[0].upper(),
                }
            })
        return JsonResponse({'success': False, 'error': 'Invalid password'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No account found with this email'}, status=404)


@csrf_exempt
@require_POST
def api_register(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        return JsonResponse({'success': False, 'error': 'All fields required'}, status=400)
    if len(password) < 6:
        return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email already registered'}, status=409)

    username = email.split('@')[0]
    base_username = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    parts = name.split(' ', 1)
    first = parts[0]
    last = parts[1] if len(parts) > 1 else ''
    user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=first, last_name=last)
    UserProfile.objects.create(user=user, avatar_initial=first[0].upper())

    # Create default home address
    Address.objects.create(
        user=user, label='home',
        full_address='Kalaburagi, Karnataka 585101',
        city='Kalaburagi', pincode='585101', is_default=True
    )

    login(request, user)
    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'is_admin': False,
            'initial': first[0].upper(),
        }
    })


@csrf_exempt
@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})


@require_GET
def api_me(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user)
        total_spent = orders.aggregate(s=Sum('total'))['s'] or 0
        active = orders.filter(status__in=['confirmed', 'preparing', 'out_for_delivery']).count()
        addresses = list(user.addresses.values('label', 'full_address', 'city', 'pincode', 'is_default'))
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'is_admin': user.email == 'admin@quickbite.com',
                'initial': (user.get_full_name() or user.username)[0].upper(),
                'total_orders': orders.count(),
                'total_spent': total_spent,
                'active_orders': active,
                'addresses': addresses,
            }
        })
    return JsonResponse({'authenticated': False})


# ─── RESTAURANTS API ───────────────────────────────────────────────────────────

@require_GET
def api_restaurants(request):
    qs = Restaurant.objects.prefetch_related('cuisines').all()

    # Filters
    cuisine = request.GET.get('cuisine')
    filter_type = request.GET.get('filter')
    search = request.GET.get('search', '').strip()

    if cuisine and cuisine != 'All':
        qs = qs.filter(cuisines__name__icontains=cuisine)
    if filter_type == 'rating':
        qs = qs.filter(rating__gte=4.0)
    elif filter_type == 'fast':
        qs = qs.filter(delivery_time_max__lte=30)
    elif filter_type == 'pure-veg':
        qs = qs.filter(is_veg=True)
    elif filter_type == 'offer':
        qs = qs.filter(has_offer=True)
    elif filter_type == 'budget':
        qs = qs.filter(min_order__lte=200)
    elif filter_type == 'new':
        qs = qs.order_by('-created_at')

    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(address__icontains=search))

    data = []
    for r in qs:
        data.append({
            'id': r.id,
            'name': r.name,
            'address': r.address,
            'image_url': r.image_url,
            'rating': float(r.rating),
            'delivery_time': r.delivery_time_display,
            'delivery_fee': r.delivery_fee_display,
            'min_order': r.min_order,
            'is_veg': r.is_veg,
            'is_open': r.is_open,
            'is_featured': r.is_featured,
            'has_offer': r.has_offer,
            'offer_text': r.offer_text,
            'badge': r.badge,
            'cuisines': [c.name for c in r.cuisines.all()],
        })
    return JsonResponse({'restaurants': data})


@require_GET
def api_restaurant_detail(request, pk):
    r = get_object_or_404(Restaurant, pk=pk)
    items = r.menu_items.filter(is_available=True).values(
        'id', 'name', 'description', 'price', 'category',
        'image_url', 'is_veg', 'is_bestseller', 'rating', 'calories', 'spice_level'
    )
    # Group by category
    from collections import defaultdict
    grouped = defaultdict(list)
    for item in items:
        grouped[item['category']].append(item)

    return JsonResponse({
        'restaurant': {
            'id': r.id,
            'name': r.name,
            'description': r.description,
            'address': r.address,
            'image_url': r.image_url,
            'rating': float(r.rating),
            'delivery_time': r.delivery_time_display,
            'delivery_fee': r.delivery_fee_display,
            'delivery_fee_amount': r.delivery_fee,
            'min_order': r.min_order,
            'is_veg': r.is_veg,
            'is_open': r.is_open,
            'badge': r.badge,
            'cuisines': [c.name for c in r.cuisines.all()],
        },
        'menu': dict(grouped),
    })


# ─── ORDERS API ────────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def api_place_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'}, status=401)

    data = json.loads(request.body)
    restaurant_id = data.get('restaurant_id')
    items = data.get('items', [])  # [{id, name, price, qty}]
    payment = data.get('payment', 'cod')
    address = data.get('address', 'Kalaburagi, Karnataka 585101')

    if not items:
        return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)

    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    subtotal = sum(i['price'] * i['qty'] for i in items)
    delivery_fee = restaurant.delivery_fee
    taxes = int(subtotal * 0.05)
    total = subtotal + delivery_fee + taxes

    order = Order.objects.create(
        user=request.user,
        restaurant=restaurant,
        status='confirmed',
        payment_method=payment,
        delivery_address=address,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        taxes=taxes,
        total=total,
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            menu_item_id=item.get('id'),
            name=item['name'],
            price=item['price'],
            quantity=item['qty'],
        )

    return JsonResponse({
        'success': True,
        'order_id': order.id,
        'order': {
            'id': order.id,
            'restaurant': restaurant.name,
            'total': total,
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'taxes': taxes,
            'status': order.status,
            'payment': payment,
            'estimated_minutes': 35,
            'courier': order.courier_name,
        }
    })


@require_GET
def api_order_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({'orders': []})

    orders = Order.objects.filter(user=request.user).select_related('restaurant').prefetch_related('items').order_by('-created_at')[:20]
    data = []
    for o in orders:
        data.append({
            'id': o.id,
            'restaurant': o.restaurant.name,
            'status': o.status,
            'total': o.total,
            'items_count': o.items.count(),
            'created_at': o.created_at.strftime('%b %d, %I:%M %p'),
            'items': [{'name': i.name, 'qty': i.quantity, 'price': i.price} for i in o.items.all()],
        })
    return JsonResponse({'orders': data})


# ─── FAVOURITES API ────────────────────────────────────────────────────────────

@csrf_exempt
def api_toggle_favourite(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'}, status=401)

    data = json.loads(request.body)
    restaurant_id = data.get('restaurant_id')
    fav, created = Favourite.objects.get_or_create(
        user=request.user, restaurant_id=restaurant_id
    )
    if not created:
        fav.delete()
        return JsonResponse({'success': True, 'favourited': False})
    return JsonResponse({'success': True, 'favourited': True})


@require_GET
def api_favourites(request):
    if not request.user.is_authenticated:
        return JsonResponse({'favourites': []})
    ids = list(Favourite.objects.filter(user=request.user).values_list('restaurant_id', flat=True))
    return JsonResponse({'favourites': ids})


# ─── ADDRESS API ───────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def api_update_address(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'}, status=401)

    data = json.loads(request.body)
    city = data.get('city', 'Kalaburagi')
    pincode = data.get('pincode', '585101')
    full_address = data.get('address', f'{city} {pincode}')

    addr, _ = Address.objects.get_or_create(
        user=request.user, label='home',
        defaults={'city': city, 'pincode': pincode, 'full_address': full_address, 'is_default': True}
    )
    addr.city = city
    addr.pincode = pincode
    addr.full_address = full_address
    addr.save()
    return JsonResponse({'success': True, 'address': full_address})


# ─── PROMO CODE API ────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def api_apply_promo(request):
    data = json.loads(request.body)
    code = data.get('code', '').strip().upper()
    order_total = data.get('total', 0)

    try:
        promo = PromoCode.objects.get(code=code, is_active=True)
        if promo.min_order > order_total:
            return JsonResponse({'success': False, 'error': f'Minimum order ₹{promo.min_order} required'})
        discount = promo.discount_flat if promo.discount_flat else int(order_total * promo.discount_percent / 100)
        return JsonResponse({'success': True, 'discount': discount, 'description': promo.description})
    except PromoCode.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid promo code'})


# ─── ADMIN API ─────────────────────────────────────────────────────────────────

@require_GET
def api_admin_stats(request):
    if not request.user.is_authenticated or request.user.email != 'admin@quickbite.com':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today)
    revenue_today = orders_today.aggregate(s=Sum('total'))['s'] or 0
    active_restaurants = Restaurant.objects.filter(is_open=True).count()
    total_users = User.objects.count()

    recent_orders = Order.objects.select_related('user', 'restaurant').order_by('-created_at')[:8]
    orders_data = [{
        'id': o.id,
        'user': o.user.get_full_name() or o.user.username,
        'restaurant': o.restaurant.name,
        'total': o.total,
        'status': o.status,
        'time': o.created_at.strftime('%I:%M %p'),
    } for o in recent_orders]

    restaurants = Restaurant.objects.order_by('-total_orders')[:6]
    rest_data = [{
        'id': r.id,
        'name': r.name,
        'image_url': r.image_url,
        'total_orders': r.total_orders,
        'rating': float(r.rating),
        'is_open': r.is_open,
    } for r in restaurants]

    # Weekly revenue (mock data for chart)
    weekly = [42000, 55000, 38000, 68000, 72000, 61000, int(revenue_today) or 48000]

    return JsonResponse({
        'kpis': {
            'orders_today': orders_today.count(),
            'revenue_today': revenue_today,
            'active_restaurants': active_restaurants,
            'total_users': total_users,
        },
        'recent_orders': orders_data,
        'top_restaurants': rest_data,
        'weekly_revenue': weekly,
    })


# ─── SEARCH API ────────────────────────────────────────────────────────────────

@require_GET
def api_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})

    restaurants = Restaurant.objects.filter(
        Q(name__icontains=q) | Q(address__icontains=q)
    )[:5]

    items = MenuItem.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        is_available=True
    ).select_related('restaurant')[:5]

    results = []
    for r in restaurants:
        results.append({'type': 'restaurant', 'id': r.id, 'name': r.name, 'meta': r.address, 'image': r.image_url})
    for i in items:
        results.append({'type': 'item', 'id': i.restaurant_id, 'name': i.name,
                        'meta': f'₹{i.price} · {i.restaurant.name}', 'image': i.image_url})

    return JsonResponse({'results': results})
