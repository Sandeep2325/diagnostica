from app1.models import city,test
def context_processor(request):
    cityy=city.objects.filter(active=True)
    tests=test.objects.all()
    context = {
        "cityy":cityy,
        "tests":tests
    }
    return context 