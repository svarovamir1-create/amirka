from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator

# ======== ПРОДУКТЫ ========
def home(request):
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {"categories": categories})


def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=category, is_active=True)

    # 🔍 Поиск
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # 💰 Фильтр цены
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    # 📦 В наличии
    if request.GET.get("in_stock") == "1":
        qs = qs.filter(stock__gt=0)

    # 🔽 Сортировка
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")
    else:
        qs = qs.order_by("name")

    # 📄 Пагинация
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    qs_params = params.urlencode()

    return render(request, "catalog/product_list.html", {
        "category": category,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})


# ======== КОРЗИНА НА SESSION ========
def get_cart(request):
    """Возвращает корзину из сессии"""
    return request.session.setdefault('cart', {})


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product_id)
    quantity = cart.get(product_id, 0)

    if product.stock == 0:
        # нельзя добавить товар без stock
        return redirect('catalog:product_detail', slug=product.slug)

    if quantity < product.stock:
        cart[product_id] = quantity + 1

    request.session.modified = True
    return redirect('catalog:cart')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session.modified = True
    return redirect('catalog:cart')


def increase_quantity(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    product_id = str(product_id)

    if cart.get(product_id, 0) < product.stock:
        cart[product_id] += 1

    request.session.modified = True
    return redirect('catalog:cart')


def decrease_quantity(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]

    request.session.modified = True
    return redirect('catalog:cart')


def cart_view(request):
    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_sum = 0
    total_quantity = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        total_sum += total
        total_quantity += quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
        'total_positions': len(cart_items)
    })
# ======== АККАУНТЫ ========
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from orders.models import Order


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("catalog:home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("catalog:home")