import json
from projectBakuna.exceptions import InvalidNumber, MaxEntryException
import time
from django.http.response import HttpResponse, JsonResponse
from rest_framework import status
from projectBakuna.environment import TABLES
from API.services import CreateService
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class FormsAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data.get('personal_information', None)
            response = request.data.get('response', None)
            if data is not None and request is not None:
                rID, PIN = CreateService.handle(response, data)
                if rID is not None and PIN is not None:
                    return JsonResponse({"user": {"rID": rID, "PIN": PIN}}, status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"errors": {"error": "Mobile Number must be verified."}}, status=status.HTTP_404_NOT_FOUND)
        except InvalidNumber as e:
            return JsonResponse({"errors": {"error": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        except MaxEntryException as e:
            return JsonResponse({"errors": {"error": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
