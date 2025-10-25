from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from .models import Tire, TireManager


def tire_list(request):
    """List of tires with search, filtering and sorting"""
    tires: TireManager = Tire.objects.all()

    # Search
    search = request.GET.get("search", "")
    if search:
        tires = tires.search(search)

    brand = request.GET.get("brand", "")
    if brand:
        tires = tires.by_brand(brand)

    season = request.GET.get("season", "")
    if season:
        tires = tires.by_season(season)

    diameter = request.GET.get("diameter", "")
    if diameter:
        tires = tires.by_diameter(diameter)

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    if min_price and max_price:
        tires = tires.by_price_range(float(min_price), float(max_price))

    sort_by = request.GET.get("sort_by", "-created_at")
    valid_sorts = ["-created_at", "created_at", "price", "-price", "brand"]
    if sort_by in valid_sorts:
        tires = tires.order_by(sort_by)

    in_stock_only = request.GET.get("in_stock", "")
    if in_stock_only:
        tires = tires.in_stock()

    # PAGINATION (12 products per page)
    paginator = Paginator(tires, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # GET UNIQUE VALUES FOR THE FILTERS
    all_tires: TireManager = Tire.objects.all()
    brands = sorted(all_tires.values_list("brand", flat=True).distinct())
    seasons = all_tires.values_list("season", flat=True).distinct()
    diameters = sorted(all_tires.values_list("diameter", flat=True).distinct())

    min_price_db = all_tires.aggregate(models.Min("price"))["price__min"] or 0
    max_price_db = all_tires.aggregate(models.Max("price"))["price__max"] or 0

    context = {
        "page_obj": page_obj,
        "tires": page_obj.object_list,
        "brands": brands,
        "seasons": seasons,
        "diameters": diameters,
        "min_price_db": min_price_db,
        "max_price_db": max_price_db,
        "current_search": search,
        "current_brand": brand,
        "current_seasons": seasons,
        "current_diameter": diameter,
    }

    return render(request, "tires/tire_list.html", context=context)


def tire_detail(request, slug):
    """Parts of one tire"""
    tire = get_object_or_404(Tire, slug=slug)

    related = Tire.objects.filter(brand=tire.brand, season=tire.season).exclude(
        id=tire.id
    )[:4]

    context = {
        "tire": tire,
        "related": related,
    }

    return render(request, "tires/tire_detail.html", context=context)
