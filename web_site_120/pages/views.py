from django.shortcuts import render
from disks.models import Disk
from tires.models import Tire


def home(request):
    """Main Page"""
    latest_disks = Disk.objects.all()[0:6]
    latest_tires = Tire.objects.all()[0:6]

    return render(
        request,
        "pages/home.html",
        {
            "disks": latest_disks,
            "tires": latest_tires,
        },
    )
