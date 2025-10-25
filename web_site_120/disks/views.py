from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from .models import Disk, DiskManager


def disk_list(request):
    """List of disks with search, filtering, and sorting"""
    disks: DiskManager = Disk.objects.all()

    # Search
    search = request.GET.get("search", "")
    if search:
        disks = disks.search(search)

    brand = request.GET.get("brand", "")
    if brand:
        disks = disks.by_brand(brand)

    diameter = request.GET.get("diameter", "")
    if diameter:
        disks = disks.by_diameter(diameter)

    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    if min_price and max_price:
        disks = disks.by_price_range(float(min_price), float(max_price))

    sort_by = request.GET.get("sort_by", "-created_at")
    valid_sorts = ["-created_at", "created_at", "price", "-price", "brand"]
    if sort_by in valid_sorts:
        disks = disks.order_by(sort_by)

    is_stock_only = request.GET.get("in_stock", "")
    if is_stock_only:
        disks = disks.in_stock()

    # PAGINATION (12 products per page)
    paginator = Paginator(disks, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # GET UNIQUE VALUES FOR THE FILTERS
    all_disks: DiskManager = Disk.objects.all()
    brands = sorted(all_disks.values_list("brand", flat=True).distinct())
    diameters = sorted(all_disks.values_list("diameter", flat=True).distinct())

    min_price_db = all_disks.aggregate(models.Min("price"))["price__min"] or 0
    max_price_db = all_disks.aggregate(models.Max("price"))["price__max"] or 0

    context = {
        "page_obj": page_obj,
        "disks": page_obj.object_list,
        "brands": brands,
        "diameters": diameters,
        "min_price_db": min_price_db,
        "max_price_db": max_price_db,
        "current_search": search,
        "current_brand": brand,
        "current_diameter": diameter,
    }

    return render(request, "disk/disk_list.html", context=context)


def disk_detail(request, slug):
    """Details of one disk"""
    disk = get_object_or_404(Disk, slug=slug)

    related = Disk.objects.filter(brand=disk.brand).exclude(id=disk.id)[:4]

    context = {
        "disk": disk,
        "related": related,
    }

    return render(request, "disks/disk_detail.html", context=context)
