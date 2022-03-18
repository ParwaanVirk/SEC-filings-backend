from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from login.models import * 
from login.serialzers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        requester = {
            'email': request.data.get('email', None),
            'username': request.data.get('username', None),
            'password' : request.data.get('password', None), 
        }
        userType = request.data.get('interviewer', None)
        serializer = RegistrationSerializer(data = requester)
        data = {}
        if userType == "YES":
            if serializer.is_valid():
                Caccount = serializer.save()
                Caccount.is_assessor = True
                Caccount.save()
                data['response'] = "Successfully registered a new user"
                status = 200
            else:
                data = serializer.errors
                status = 422

        elif userType == "NO":
            if serializer.is_valid():
                Caccount = serializer.save()
                Caccount.is_candidate = True
                Caccount.save()
                data['response'] = "Successfully registered a new user"
                status = 200
            else:
                data = serializer.errors
                status = 422

        else:
            data = "Wrong data passed"
            status = 423
        
        return Response(data, status)


class UserDataView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cuser = request.user
        cuserSerialized = UserSerializer(cuser)
        return Response(data = cuserSerialized.data, status=200)



    
class PasswordReset(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            serializer = ChangePasswordSerializer(data = request.data)
            if serializer.is_valid():
                oldPassword = serializer.validated_data['old_password']
                newPassword = serializer.validated_data['new_password']
                if not cuser.check_password(oldPassword):
                    return Response(data = "Old password was wrong", status=400)
                elif oldPassword == newPassword:
                    return Response(data= "Cannot keep same password", status = 420)
                else:
                    cuser.set_password(newPassword)
                    print(newPassword)
                    cuser.save()
                    return Response(status = 200, data = "Successfully updated password")
            else:
                return Response(data = serializer.errors, status = 430)
        else:
            return Response(data = "Cuser does not exist", status = 404)