from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from login.models import Token
from login.serializers import ChangePasswordSerializer, RegistrationSerializer, UserSerializer

# Create your views here.

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        requester = {
            'email': request.data.get('email', None),
            'username': request.data.get('username', None),
            'password' : request.data.get('password', None),
        }
        serializer = RegistrationSerializer(data = requester)
        data = {}
        if serializer.is_valid():
            current_account = serializer.save()
            data['token'] = Token.objects.filter(user = current_account)[0].key
            data['registered'] = True
            data['errors'] = None
            status = 200
        else:
            data['registered'] = False
            data['errors'] = serializer.errors
            status = 422

        return Response(data, status)


class UserDataView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cuser = request.user
        response_dict = {}
        cuserSerialized = UserSerializer(cuser)
        response_dict['data'] = cuserSerialized.data
        return Response(data = response_dict, status=200)




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
                    cuser.save()
                    return Response(status = 200, data = "Successfully updated password")
            else:
                return Response(data = serializer.errors, status = 430)
        else:
            return Response(data = "Cuser does not exist", status = 404)