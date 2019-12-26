import json
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
from rest_framework import status

@csrf_exempt
@require_http_methods(["GET", "POST", "PATCH"])
def index(request):
    keys = request.GET.get('keys', None)
    if request.method == "GET" and not keys:
        data_keys = cache.keys('*')
        data = cache.get_many(data_keys)

        if len(data):
            cache.touch(data_keys, settings.CACHE_TTL)

        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)

    elif request.method == "GET" and keys:
        try:
            keys = keys.split(",")
            data = cache.get_many(keys)

            if len(data) == 0:
                return HttpResponse(json.dumps(data), status=status.HTTP_404_NOT_FOUND)
            elif len(data) != len(keys):
                cache.touch(keys, settings.CACHE_TTL)
                return HttpResponse(json.dumps(data), status=status.HTTP_207_MULTI_STATUS)
            else:
                cache.touch(keys, settings.CACHE_TTL)
                return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)
        except Exception:
            return HttpResponse("Unprocessable Entity.", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            failed_keys = cache.set_many(data, settings.CACHE_TTL)

            if failed_keys:
                return HttpResponse("Keys {} have not saved.".format(failed_keys, data), status=status.HTTP_207_MULTI_STATUS)

            return HttpResponse("Data  {}, saved successfully.".format(data), status=status.HTTP_201_CREATED)

        except Exception:
            return HttpResponse("Unprocessable Entity.", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        try:
            data = json.loads(request.body)
            failed_keys = cache.set_many(data, settings.CACHE_TTL)

            if failed_keys:
                return HttpResponse("Keys {} have not updated.".format(failed_keys, data), status=status.HTTP_207_MULTI_STATUS)

            return HttpResponse("Data  {}, updated successfully.".format(data), status=status.HTTP_202_ACCEPTED)

        except Exception:
            return HttpResponse("Unprocessable Entity.", status=status.HTTP_400_BAD_REQUEST)
