from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {"categories": categories})


from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator


def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    qs = Product.objects.filter(category=category, is_active=True)

    # 🔍 ПОИСК
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # 💰 ФИЛЬТР ЦЕНЫ
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    # 📦 В НАЛИЧИИ
    if request.GET.get("in_stock") == "1":
        qs = qs.filter(stock__gt=0)

    # 🔽 СОРТИРОВКА
    sort = request.GET.get("sort", "")

    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")
    else:
        qs = qs.order_by("name")

    # 📄 ПАГИНАЦИЯ
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    # чтобы фильтры сохранялись
    params = request.GET.copy()
    params.pop("page", None)
    qs_params = params.urlencode()

    return render(request, "catalog/product_list.html", {
        "category": category,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })
from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, "catalog/product_detail.html", {
        "product": product
    })