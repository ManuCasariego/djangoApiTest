from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.giveAccommodations import get_accommodations


@csrf_exempt
def accommodations(request):
    """
    List all code snippets, or create a new snippet.
    """

    return JsonResponse(get_accommodations({'ip': get_client_ip(request)}), safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_ip(request):
    return request.get_host()
