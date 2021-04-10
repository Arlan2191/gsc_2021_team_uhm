from requests.api import get
from API.services import AuthUserService
from django.http.response import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from API.serializers import RegistrationSerializer, LoginSerializer, UserSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user = request.data.get('user', {})
            type = request.data.get('type', None)
            _ = AuthUserService.register(type, **user)
            return JsonResponse({"status": 200}, status=status.HTTP_200_OK)
        except:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user = request.data.get('user', {})
            data = AuthUserService.login(user)
            return JsonResponse({"user": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request):
        serializer = self.serializer_class(request.user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"user": serializer.data}, status=status.HTTP_200_OK)
