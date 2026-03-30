from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Restaurant, MenuItem, Cuisine, PromoCode, UserProfile, Address


class Command(BaseCommand):
    help = 'Seed QuickBite database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🍽️  Seeding QuickBite database...')

        # ── Cuisines ──────────────────────────────────────────────────────────
        cuisines_data = [
            ('Pizza', 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=120&h=120&fit=crop', 42),
            ('Sushi', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=120&h=120&fit=crop', 18),
            ('Burger', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=120&h=120&fit=crop', 35),
            ('Biryani', 'https://images.unsplash.com/photo-1563379091339-03246963d96c?w=120&h=120&fit=crop', 28),
            ('Chinese', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=120&h=120&fit=crop', 21),
            ('Desserts', 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=120&h=120&fit=crop', 29),
            ('South Indian', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=120&h=120&fit=crop', 33),
            ('Thali', 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=120&h=120&fit=crop', 15),
            ('North Indian', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=120&h=120&fit=crop', 40),
        ]
        cuisines = {}
        for name, img, count in cuisines_data:
            c, _ = Cuisine.objects.get_or_create(name=name, defaults={'image_url': img, 'kitchen_count': count})
            cuisines[name] = c
        self.stdout.write('  ✓ Cuisines seeded')

        # ── Restaurants ───────────────────────────────────────────────────────
        restaurants_data = [
            {
                'id_key': 'spice_garden',
                'name': 'Spice Garden',
                'description': 'Authentic North Indian cuisine with rich gravies, fresh tandoor breads and slow-cooked biryanis. A Kalaburagi institution since 1998.',
                'address': 'Station Road, Kalaburagi 585101',
                'image_url': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=400&fit=crop&q=80',
                'rating': 4.9,
                'delivery_time_min': 25, 'delivery_time_max': 30,
                'delivery_fee': 0, 'min_order': 200,
                'is_veg': False, 'is_featured': True, 'has_offer': True,
                'offer_text': '20% OFF on orders above ₹500',
                'badge': 'TOP RATED', 'total_orders': 1240,
                'cuisines': ['North Indian', 'Biryani'],
            },
            {
                'id_key': 'bella_italia',
                'name': 'Bella Italia',
                'description': 'Authentic Italian kitchen serving wood-fired pizzas, creamy pastas and house-made gelato.',
                'address': 'MG Road, Kalaburagi 585102',
                'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=400&fit=crop&q=80',
                'rating': 4.7,
                'delivery_time_min': 30, 'delivery_time_max': 40,
                'delivery_fee': 49, 'min_order': 300,
                'is_veg': False, 'is_featured': True, 'has_offer': False,
                'offer_text': '', 'badge': 'PREMIUM', 'total_orders': 890,
                'cuisines': ['Pizza'],
            },
            {
                'id_key': 'burger_barn',
                'name': 'Burger Barn',
                'description': 'Juicy smash burgers, loaded fries and creamy shakes. The city\'s favourite American joint.',
                'address': 'City Centre Mall, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&h=400&fit=crop&q=80',
                'rating': 4.7,
                'delivery_time_min': 15, 'delivery_time_max': 20,
                'delivery_fee': 29, 'min_order': 150,
                'is_veg': False, 'is_featured': False, 'has_offer': True,
                'offer_text': 'Buy 2 Get 1 Free on Combo Meals',
                'badge': 'FAST', 'total_orders': 2100,
                'cuisines': ['Burger'],
            },
            {
                'id_key': 'biryani_house',
                'name': 'The Biryani House',
                'description': 'Dum-cooked biryanis with fragrant basmati rice, tender meat and aromatic spices. Hyderabadi style.',
                'address': 'Jagat Circle, Kalaburagi 585103',
                'image_url': 'https://images.unsplash.com/photo-1563379091339-03246963d96c?w=800&h=400&fit=crop&q=80',
                'rating': 4.8,
                'delivery_time_min': 30, 'delivery_time_max': 45,
                'delivery_fee': 0, 'min_order': 250,
                'is_veg': False, 'is_featured': True, 'has_offer': True,
                'offer_text': 'Free Raita on orders above ₹400',
                'badge': 'POPULAR', 'total_orders': 1850,
                'cuisines': ['Biryani', 'North Indian'],
            },
            {
                'id_key': 'green_leaf',
                'name': 'Green Leaf',
                'description': 'Pure vegetarian restaurant serving healthy, wholesome meals from Karnataka and across India.',
                'address': 'Nehru Gunj, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&h=400&fit=crop&q=80',
                'rating': 4.5,
                'delivery_time_min': 20, 'delivery_time_max': 30,
                'delivery_fee': 0, 'min_order': 150,
                'is_veg': True, 'is_featured': False, 'has_offer': False,
                'offer_text': '', 'badge': 'PURE VEG', 'total_orders': 670,
                'cuisines': ['South Indian', 'Thali', 'North Indian'],
            },
            {
                'id_key': 'dragon_palace',
                'name': 'Dragon Palace',
                'description': 'Indo-Chinese fusion — manchurian, noodles, fried rice and dim sum crafted with bold flavours.',
                'address': 'Super Market, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=400&fit=crop&q=80',
                'rating': 4.3,
                'delivery_time_min': 25, 'delivery_time_max': 35,
                'delivery_fee': 39, 'min_order': 200,
                'is_veg': False, 'is_featured': False, 'has_offer': True,
                'offer_text': '15% OFF on first order',
                'badge': 'NEW', 'total_orders': 320,
                'cuisines': ['Chinese'],
            },
            {
                'id_key': 'sweet_corner',
                'name': 'Sweet Corner',
                'description': 'Artisan desserts, Indian mithai, ice creams and bakery fresh from the oven every morning.',
                'address': 'Bhavani Nagar, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=800&h=400&fit=crop&q=80',
                'rating': 4.6,
                'delivery_time_min': 20, 'delivery_time_max': 30,
                'delivery_fee': 20, 'min_order': 100,
                'is_veg': True, 'is_featured': False, 'has_offer': False,
                'offer_text': '', 'badge': '', 'total_orders': 540,
                'cuisines': ['Desserts'],
            },
            {
                'id_key': 'sushi_sakura',
                'name': 'Sushi Sakura',
                'description': 'Premium Japanese fusion — sushi rolls, sashimi, ramen and sake. An authentic Tokyo experience.',
                'address': 'Downtown, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&h=400&fit=crop&q=80',
                'rating': 4.8,
                'delivery_time_min': 35, 'delivery_time_max': 40,
                'delivery_fee': 49, 'min_order': 400,
                'is_veg': False, 'is_featured': True, 'has_offer': False,
                'offer_text': '', 'badge': 'PREMIUM', 'total_orders': 410,
                'cuisines': ['Sushi'],
            },
            {
                'id_key': 'dosa_darbar',
                'name': 'Dosa Darbar',
                'description': 'Crispy dosas, fluffy idlis, vada and sambar that transport you to a Chennai tiffin room.',
                'address': 'Gandhi Nagar, Kalaburagi',
                'image_url': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&h=400&fit=crop&q=80',
                'rating': 4.6,
                'delivery_time_min': 15, 'delivery_time_max': 25,
                'delivery_fee': 0, 'min_order': 100,
                'is_veg': True, 'is_featured': False, 'has_offer': True,
                'offer_text': '₹30 OFF on breakfast orders',
                'badge': 'FAST', 'total_orders': 960,
                'cuisines': ['South Indian'],
            },
        ]

        for rd in restaurants_data:
            cuisine_names = rd.pop('cuisines', [])
            rd.pop('id_key')
            r, created = Restaurant.objects.get_or_create(name=rd['name'], defaults=rd)
            if not created:
                for k, v in rd.items():
                    setattr(r, k, v)
                r.save()
            for cn in cuisine_names:
                if cn in cuisines:
                    r.cuisines.add(cuisines[cn])

        self.stdout.write('  ✓ Restaurants seeded')

        # ── Menu Items ────────────────────────────────────────────────────────
        spice_garden = Restaurant.objects.get(name='Spice Garden')
        bella = Restaurant.objects.get(name='Bella Italia')
        burger = Restaurant.objects.get(name='Burger Barn')
        biryani = Restaurant.objects.get(name='The Biryani House')
        green = Restaurant.objects.get(name='Green Leaf')
        sushi = Restaurant.objects.get(name='Sushi Sakura')
        dosa = Restaurant.objects.get(name='Dosa Darbar')

        menu_items = [
            # Spice Garden
            (spice_garden, 'Butter Chicken', 'Tender chicken in rich tomato-cream gravy', 320, 'main', True, True,
             'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop', False, 1, 4.9, 480),
            (spice_garden, 'Dal Makhani', 'Slow-cooked black lentils in buttery tomato gravy', 220, 'main', False, True,
             'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=300&fit=crop', True, 0, 4.7, 350),
            (spice_garden, 'Garlic Naan', 'Freshly baked leavened bread with garlic butter', 60, 'breads', False, False,
             'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop', True, 0, 4.5, 180),
            (spice_garden, 'Chicken Biryani', 'Aromatic basmati rice with tender chicken', 380, 'main', True, True,
             'https://images.unsplash.com/photo-1563379091339-03246963d96c?w=400&h=300&fit=crop', False, 2, 4.9, 620),
            (spice_garden, 'Paneer Tikka', 'Grilled cottage cheese with peppers in spicy marinade', 280, 'starter', False, True,
             'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop', True, 1, 4.8, 320),
            (spice_garden, 'Gulab Jamun', 'Soft milk dumplings in rose syrup — 2 pieces', 80, 'dessert', False, False,
             'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop', True, 0, 4.6, 240),

            # Bella Italia
            (bella, 'Margherita Pizza', 'San Marzano tomato, fresh mozzarella, basil', 420, 'main', False, True,
             'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop', True, 0, 4.8, 680),
            (bella, 'Spaghetti Carbonara', 'Egg, Pecorino, guanciale, black pepper', 480, 'main', False, False,
             'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400&h=300&fit=crop', False, 0, 4.7, 720),
            (bella, 'Tiramisu', 'Classic Italian coffee dessert with mascarpone', 220, 'dessert', False, True,
             'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop', True, 0, 4.9, 380),
            (bella, 'Garlic Bread', 'Toasted ciabatta with herb butter', 150, 'starter', False, False,
             'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?w=400&h=300&fit=crop', True, 0, 4.5, 220),

            # Burger Barn
            (burger, 'Classic Smash Burger', 'Double smash patty, cheddar, pickles, special sauce', 299, 'main', True, True,
             'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop', False, 0, 4.8, 720),
            (burger, 'Crispy Chicken Burger', 'Crispy fried chicken, coleslaw, jalapeños', 279, 'main', True, False,
             'https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=300&fit=crop', False, 1, 4.7, 680),
            (burger, 'Loaded Fries', 'Seasoned fries with cheese sauce and jalapeños', 149, 'sides', False, True,
             'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=300&fit=crop', True, 1, 4.6, 480),
            (burger, 'Oreo Shake', 'Creamy Oreo milkshake, extra thick', 179, 'drinks', False, False,
             'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop', True, 0, 4.8, 520),

            # Biryani House
            (biryani, 'Hyderabadi Chicken Biryani', 'Dum-cooked with saffron rice, caramelized onions', 380, 'main', True, True,
             'https://images.unsplash.com/photo-1563379091339-03246963d96c?w=400&h=300&fit=crop', False, 2, 4.9, 680),
            (biryani, 'Mutton Biryani', 'Slow-cooked mutton with fragrant long-grain rice', 450, 'main', True, False,
             'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop', False, 2, 4.8, 720),
            (biryani, 'Veg Dum Biryani', 'Garden vegetables with aromatic basmati', 280, 'main', False, False,
             'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop', True, 1, 4.5, 520),
            (biryani, 'Mirchi Ka Salan', 'Hyderabadi green chilli curry — perfect accompaniment', 120, 'sides', False, False,
             'https://images.unsplash.com/photo-1574653853027-5382a3d23a15?w=400&h=300&fit=crop', True, 2, 4.6, 180),

            # Green Leaf
            (green, 'Thali Deluxe', 'Dal, sabzi, rice, 3 rotis, raita, salad & sweet', 220, 'main', False, True,
             'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop', True, 0, 4.7, 680),
            (green, 'Paneer Kadhai', 'Cottage cheese stir-fried with peppers and spices', 260, 'main', False, False,
             'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop', True, 1, 4.5, 420),

            # Sushi Sakura
            (sushi, 'Dragon Roll', 'Spicy tuna, avocado, cucumber, tobiko', 520, 'main', True, True,
             'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&h=300&fit=crop', False, 2, 4.9, 420),
            (sushi, 'Miso Ramen', 'Rich miso broth, chashu pork, soft egg, nori', 480, 'main', False, False,
             'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop', False, 1, 4.8, 580),
            (sushi, 'Edamame', 'Steamed salted soybeans — classic starter', 180, 'starter', False, True,
             'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=400&h=300&fit=crop', True, 0, 4.4, 120),

            # Dosa Darbar
            (dosa, 'Masala Dosa', 'Crispy rice crepe with spiced potato filling', 120, 'main', False, True,
             'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400&h=300&fit=crop', True, 1, 4.8, 380),
            (dosa, 'Idli Sambar (4pcs)', 'Steamed rice cakes with lentil soup & chutneys', 90, 'main', False, False,
             'https://images.unsplash.com/photo-1625398407796-82650a8c0855?w=400&h=300&fit=crop', True, 0, 4.7, 260),
            (dosa, 'Filter Coffee', 'South Indian drip coffee with frothy milk', 60, 'drinks', False, True,
             'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop', True, 0, 4.9, 80),
            (dosa, 'Uttapam', 'Thick rice pancake topped with onion, tomato, coriander', 110, 'main', False, False,
             'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop', True, 0, 4.6, 320),
        ]

        for (rest, name, desc, price, cat, bs, avail, img, is_veg_item, spice, rating, cal) in menu_items:
            MenuItem.objects.get_or_create(
                restaurant=rest, name=name,
                defaults={
                    'description': desc, 'price': price, 'category': cat,
                    'is_bestseller': bs, 'is_available': avail, 'image_url': img,
                    'is_veg': is_veg_item, 'spice_level': spice,
                    'rating': rating, 'calories': cal,
                }
            )
        self.stdout.write('  ✓ Menu items seeded')

        # ── Promo Codes ───────────────────────────────────────────────────────
        promos = [
            ('WELCOME50', '₹50 off your first order', 0, 50, 100),
            ('FEAST20', '20% off on orders above ₹500', 20, 0, 500),
            ('EPICUREAN', '₹100 off for Epicurean Club members', 0, 100, 400),
            ('SUMMER25', '25% off all orders this summer', 25, 0, 200),
        ]
        for code, desc, pct, flat, min_ord in promos:
            PromoCode.objects.get_or_create(code=code, defaults={
                'description': desc, 'discount_percent': pct,
                'discount_flat': flat, 'min_order': min_ord, 'is_active': True
            })
        self.stdout.write('  ✓ Promo codes seeded')

        # ── Admin User ────────────────────────────────────────────────────────
        if not User.objects.filter(email='admin@quickbite.com').exists():
            admin_user = User.objects.create_superuser(
                username='admin', email='admin@quickbite.com',
                password='admin123', first_name='Admin', last_name='QuickBite'
            )
            UserProfile.objects.create(user=admin_user, is_admin=True, avatar_initial='A')
            self.stdout.write('  ✓ Admin user created (admin@quickbite.com / admin123)')

        # ── Demo User ─────────────────────────────────────────────────────────
        if not User.objects.filter(email='user@quickbite.com').exists():
            demo = User.objects.create_user(
                username='demouser', email='user@quickbite.com',
                password='user123', first_name='Alex', last_name='Demo'
            )
            UserProfile.objects.create(user=demo, avatar_initial='A')
            Address.objects.create(
                user=demo, label='home',
                full_address='Kalaburagi, Karnataka 585101',
                city='Kalaburagi', pincode='585101', is_default=True
            )
            self.stdout.write('  ✓ Demo user created (user@quickbite.com / user123)')

        self.stdout.write(self.style.SUCCESS('\n✅ QuickBite database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Run: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('   Admin login: admin@quickbite.com / admin123'))
        self.stdout.write(self.style.SUCCESS('   Demo login:  user@quickbite.com / user123'))
