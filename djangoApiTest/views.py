from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.scrapGlobal import getJsonAccommodations


@csrf_exempt
def accommodations(request):
    """
    List all code snippets, or create a new snippet.
    """
    filter_dictionary = request.GET.copy()

    return JsonResponse(getJsonAccommodations(filter_dictionary), safe=False)
