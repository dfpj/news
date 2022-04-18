import random

from graphene_django.types import DjangoObjectType
import graphene
from graphql_jwt.decorators import user_passes_test, login_required
import graphql_jwt

from .models import User, Verify, Profile
from .tasks import send_email

ACTION_RECOVER_PASSWORD = 'recover_password'
ACTION_ACTIVE_USER = 'active_user'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class AccountsQuery(graphene.ObjectType):
    user = graphene.Field(UserType, email=graphene.String())

    @login_required
    def resolve_user(parent, info, **kwargs):
        if kwargs.get('email') == info.context.user.email:
            email = kwargs.get('email')
            if email is not None:
                try:
                    return User.objects.get(email=email)
                except User.DoesNotExist:
                    return None
            return None


class CreateUser(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(parent, info, email, password):
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(email=email, password=password)
            return CreateUser(ok=True)
        else:
            return CreateUser()


class SendCodeToEmail(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        email = graphene.String()

    @staticmethod
    def mutate(parent, info, email):
        try:
            User.objects.get(email=email)
            verify_code = random.randint(1001, 9999)
            Verify.objects.create(email=email, code=verify_code)
            send_email(email=email, code=verify_code)
            return SendCodeToEmail(ok=True)
        except User.DoesNotExist:
            return SendCodeToEmail()


class CheckVerifyCode(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        email = graphene.String()
        code = graphene.Int()
        action = graphene.String()

    @staticmethod
    def mutate(parent, info, email, code, action):
        try:
            user = User.objects.get(email=email)
            verify = Verify.objects.filter(email=user.email).last()
            if verify is not None:
                result = verify.check_verify(email, code)
                if result:
                    if action == ACTION_RECOVER_PASSWORD:
                        verify.allow_update_pass = True
                        verify.save()
                    elif action == ACTION_ACTIVE_USER:
                        user.is_active = True
                        user.save()
                        Verify.objects.filter(email=email).delete()
                    else:
                        return None
                return CheckVerifyCode(ok=result)
            return None
        except User.DoesNotExist:
            return CheckVerifyCode()


class ChangePassword(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(parent, info, email, password):
        try:
            user = User.objects.get(email=email)
            verify = Verify.objects.filter(email=email).last()
            if verify.allow_update_pass:
                user.set_password(password)
                user.save()
                Verify.objects.filter(email=email).delete()
            return ChangePassword(ok=verify.allow_update_pass)
        except User.DoesNotExist:
            return ChangePassword()


class CompleteProfile(graphene.Mutation):
    ok = graphene.Boolean(default_value=False)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        birthday = graphene.Date()

    @staticmethod
    @login_required
    def mutate(parent, info, **kwargs):
        try:
            profile = Profile.objects.get(user__email=info.context.user.email)
            profile.first_name = kwargs.get('first_name') if kwargs.get('first_name') else profile.first_name
            profile.last_name = kwargs.get('last_name') if kwargs.get('last_name') else profile.last_name
            profile.birthday = kwargs.get('birthday') if kwargs.get('birthday') else profile.birthday
            profile.save()
            return CompleteProfile(ok=True)
        except Profile.DoesNotExist:
            return CompleteProfile()


class AccountsMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    check_verify_code = CheckVerifyCode.Field()
    send_code_to_email = SendCodeToEmail.Field()
    change_password = ChangePassword.Field()
    complete_profile = CompleteProfile.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
