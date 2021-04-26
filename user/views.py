import http.client
import json
import random
import math


import requests 

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .models import User, PhoneOtp, Document

from django.db.models import Q

from .serializers import UserSerializer, OtpSerializer, AuthTokenSerializer, UploadDocumentSerializer, ResendOtpSerilizer
# AuthTokenSerializer, OtpSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, mixins

API_KEY = "TLRhfDsYA3NPUfmUj2fwwCu1VucPPUi0OXert6c1auui13ikIBjayUMNOZekAq",

def generateOTP() : 
    digits = "0123456789"
    OTP = "" 
    for i in range(6) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 
  

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_class = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        API_ENDPOINT = "https://termii.com/api/sms/send"
        OTP = generateOTP()
        email = data.get('email')
        phone_no = data.get('phone_no')
        dat = {
            "to": phone_no,
            "from": "N-Alert",
            "sms": f'{OTP} is your Drugstoc OTP validation code. Code is valid for 10 minutes only, one time use. Happy Procurement',
            "type": "plain",
            "channel": "dnd",
            "api_key": API_KEY,
        }
        qs = User.objects.filter(Q(email__iexact=email) | Q(phone_no__iexact=phone_no))
        if qs.exists():
            return Response({"message": "User already exist in our database", "status": 401}, status=401)
        else:
            r = requests.post(url = API_ENDPOINT, data = dat) 
            resp = r.json()
            print(resp);
            print(request.user);
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            PhoneOtp.objects.create(phone_no=phone_no, otp_code=OTP)
            serializer.save()
            return Response({"message": "your registeration was successful an otp has been sent to you to verify you account", "status": 200, "data": serializer.data, }, status=200)
        return Response({"message": "Invalid Request", "status": 400}, status=400)


class ResendOtp(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = ResendOtpSerilizer
    permission_class = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        API_ENDPOINT = "https://termii.com/api/sms/send"
        OTP = generateOTP()
        new_phone = data.get('new_phone')
        old_phone = data.get('old_phone')
        print(old_phone)
        print(new_phone)
        dat = {
            "to": new_phone,
            "from": "N-Alert",
            "sms": f'{OTP} is your Drugstoc OTP validation code. Code is valid for 10 minutes only, one time use. Happy Procurement',
            "type": "plain",
            "channel": "dnd",
            "api_key": API_KEY,
        }
        try:
            qs = User.objects.get(phone_no=old_phone)
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist in our database", "status": 401}, status=401)
        else:
            qs.phone_no = new_phone
            qs.save()
            PhoneOtp.objects.create(phone_no=new_phone, otp_code=OTP)
            r = requests.post(url = API_ENDPOINT, data = dat)
            return Response({"message": "your otp was resent successful", "status": 200, "new_number": new_phone, }, status=200)
        return Response({"message": "Invalid Request", "status": 400}, status=400)

class DocumentList(generics.CreateAPIView):
    """List all users in the system"""
    # queryset = Document.objects.all()
    serializer_class = UploadDocumentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, )

    def post(self, request, *args, **kwargs):
        serializer = UploadDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({"message": "your document has been uploaded successfuly", "status": 200 }, status=200)


class VerifyOtp(generics.CreateAPIView):
    """ Verify a new user with phone numnber or email"""
    serializer_class = OtpSerializer
    permission_class = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        otp = data.get('otp')
        phone_no = data.get('phone_no')
        print(otp)
        print(phone_no)
        try:
            cod  = PhoneOtp.objects.get(phone_no=phone_no, otp_code=otp, is_verified=False)
            print(cod)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid Otp please check and try again"}, status=422)
        else:
            cod.is_verified = True
            cod.attempts += 1
            cod.save()
            try:
                qs = User.objects.get(phone_no=phone_no)
            except ObjectDoesNotExist:
                return Response({"message":"User does not exist", "status": 404}, status=404)
            else:
                qs.is_active = True
                qs.save()
                token = Token.objects.create(user=qs);
                return Response({"message": "Your account has been verified", "token": token.key, }, status=200)


class CreateTokenView(ObtainAuthToken):
    """Create new user in the system"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retreive and return authenticated user"""
        return self.request.user


class UserList(generics.ListAPIView):
    """List all users in the system"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)