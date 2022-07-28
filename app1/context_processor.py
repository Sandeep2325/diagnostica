from app1.models import city
def context_processor(request):
    cityy=city.objects.filter(active=True)
    context = {
        "cityy":cityy
    }
    return context 