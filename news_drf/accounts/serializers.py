from rest_framework import serializers
from .models import User, Profile, Verify


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
        extra_kwargs ={
            'password':{'write_only':True,},
            'email':{'required':True},
            'is_active':{'read_only':True},
            'is_admin':{'read_only':True},
            'last_login':{'read_only':True},
            'id':{'read_only':True},
            'profile':{'read_only':True},
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,required=True)
    code = serializers.IntegerField(write_only=True,required=True)
    action = serializers.CharField(write_only=True,required=True)