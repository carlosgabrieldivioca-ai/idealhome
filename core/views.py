from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Property


def _location_data():
    districts = Property.objects.exclude(district="").values_list("district", flat=True).distinct().order_by("district")
    return districts


def home(request):
    featured = Property.objects.all()[:12]
    addresses = Property.objects.exclude(address="").values_list("address", flat=True).distinct().order_by("address")
    districts = _location_data()
    typologies = Property.objects.exclude(typology="").values_list("typology", flat=True).distinct().order_by("typology")
    return render(request, "core/home.html", {
        "featured": featured,
        "count": Property.objects.count(),
        "addresses": addresses,
        "districts": districts,
        "typologies": typologies,
    })


def properties(request):
    qs = Property.objects.all()
    q = request.GET.get("q", "").strip()
    district = request.GET.get("distrito", "").strip()
    municipality = request.GET.get("concelho", "").strip()
    parish = request.GET.get("freguesia", "").strip()
    typology = request.GET.get("tipologia", "").strip()
    min_price = request.GET.get("min", "").strip()
    max_price = request.GET.get("max", "").strip()

    if q:
        qs = qs.filter(
            Q(address__icontains=q) |
            Q(location__icontains=q) |
            Q(title__icontains=q) |
            Q(municipality__icontains=q) |
            Q(parish__icontains=q)
        )
    if district:
        qs = qs.filter(district=district)
    if municipality:
        qs = qs.filter(municipality=municipality)
    if parish:
        qs = qs.filter(parish=parish)
    if typology and typology != "Todos":
        qs = qs.filter(typology__iexact=typology)
    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    municipalities = Property.objects.exclude(municipality="")
    if district:
        municipalities = municipalities.filter(district=district)
    municipalities = municipalities.values_list("municipality", flat=True).distinct().order_by("municipality")

    parishes = Property.objects.exclude(parish="")
    if district:
        parishes = parishes.filter(district=district)
    if municipality:
        parishes = parishes.filter(municipality=municipality)
    parishes = parishes.values_list("parish", flat=True).distinct().order_by("parish")

    typologies = Property.objects.exclude(typology="").values_list("typology", flat=True).distinct().order_by("typology")
    addresses = Property.objects.exclude(address="").values_list("address", flat=True).distinct().order_by("address")

    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "core/properties.html", {
        "page": page,
        "districts": _location_data(),
        "municipalities": municipalities,
        "parishes": parishes,
        "typologies": typologies,
        "addresses": addresses,
        "q": q,
        "selected_district": district,
        "selected_municipality": municipality,
        "selected_parish": parish,
        "selected_typology": typology,
        "min_price": min_price,
        "max_price": max_price,
    })


def detail(request, pk):
    p = get_object_or_404(Property, pk=pk)
    return render(request, "core/detail.html", {"p": p, "images": p.images()})


def address_suggestions(request):
    q = request.GET.get("q", "").strip()
    qs = Property.objects.exclude(address="")
    if q:
        qs = qs.filter(address__icontains=q)
    values = qs.values_list("address", "parish", "municipality", "district").distinct().order_by("address")[:12]
    data = [{"address": a, "parish": p, "municipality": m, "district": d} for a, p, m, d in values]
    return JsonResponse(data, safe=False)
