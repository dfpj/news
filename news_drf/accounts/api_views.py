import random

from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, VerifySerializer, ProfileSerializer
from .models import User, Verify, Profile
from .tasks import send_email
from .permission import IsOwnerOrAdmin,IsOwnerProfileOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        if 'email' in request.data and 'password' in request.data:
            User.objects.create_user(email=request.data['email'],password=request.data['password'])
            return Response({'result':'ok'})
        else:
            return Response({'result':'nok'})

    def partial_update(self, request, *args, **kwargs):
        if 'email' in request.data and 'password' in request.data:
            return change_password(kwargs['id'], request.data['email'], request.data['password'])
        else:
            return super().partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerProfileOrAdmin]

    def create(self, request, *args, **kwargs):
        return Response({"result": "not allow for create profile this action is automatic after create user"})


@api_view()
def send_code_to_email(request, id):
    try:
        user = User.objects.get(id=id)
        verify_code = random.randint(1001, 9999)
        Verify.objects.create(email=user.email, code=verify_code)
        send_email(email=user.email, code=verify_code)
        return Response({"result": "Ok"})
    except User.DoesNotExist:
        return Response({"result": "Nok"})


ACTION_RECOVER_PASSWORD = 'recover_password'
ACTION_ACTIVE_USER = 'active_user'


@api_view(['POST'])
def check_verify_code(request):
    data = VerifySerializer(data=request.data)
    if data.is_valid():
        try:
            user = User.objects.get(email=data.validated_data['email'])
            verify = Verify.objects.filter(email=user.email).last()
            if verify is not None:
                result = verify.check_verify(code=data.validated_data['code'])
                if result and data.validated_data['action'] == ACTION_RECOVER_PASSWORD:
                    verify.allow_update_pass = True
                    verify.save()
                    return Response({"result": "ok"})
                elif result and data.validated_data['action'] == ACTION_ACTIVE_USER:
                    user.is_active = True
                    user.save()
                    Verify.objects.filter(email=data.validated_data['email']).delete()
                    return Response({"result": "ok"})
                return Response({"result": "Nok"})
            return Response({"result": "Nok"})
        except User.DoesNotExist:
            return Response({"result": "Nok"})
    return Response(data.errors)


def change_password(id, email, password):
    try:
        user = User.objects.get(id=id)
        verify = Verify.objects.get(email=email)
        if verify.allow_update_pass:
            user.set_password(password)
            user.save()
            verify.delete()
            return Response({"result": "Ok"})
        return Response({"result": "NOk"})
    except (User.DoesNotExist, Verify.DoesNotExist) as e:
        return Response({"result": "NOk"})
