from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.giveAccommodations import get_accommodations
from utils.scrapGlobal import getJsonAccommodations


@csrf_exempt
def accommodations(request):
    """
    List all code snippets, or create a new snippet.
    """
    # TODO: pickup the request.get items and pass them to the getJsonAccommodations
    return JsonResponse(getJsonAccommodations(), safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# TODO: Probe when up
def get_client_ip(request):
    return request.get_host()
