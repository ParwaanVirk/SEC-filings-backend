from login.models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxValueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Account
        fields = ['id', 'email', 'username',]

        

class StudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username',]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)


    def validate_new_password(self, value):
        validate_password(value)
        return value

class StudIdInputSerializer(serializers.Serializer):
    stud_id = serializers.IntegerField(required = True, validators = [MaxValueValidator(5000)])