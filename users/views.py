from .models import User
from .serializers import CreateUserSerializer, PasswordSerializer, ForgotPasswordSerializer, \
    ResetPasswordserializer, RequestCodeSerializer, UserSerializer, \
    UserProfileSerializer, UserUpdateSerializer, AccountVerifySerializer, ProfilePhotoSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.models import AccessToken
from mylib.customs import MyCustomException, email_send
from random import randint
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


class ListCreateUsers(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = {}
        email = self.request.data['email']
        data['password'] = self.request.data['password']
        data['first_name'] = self.request.data['first_name']
        data['last_name'] = self.request.data['last_name']
        data['phone_number'] = self.request.data['phone_number']
        data['email'] = email
        serializer = CreateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['username'] = email
        serializer.save()
        return Response("User created successfully", status=status.HTTP_201_CREATED)


class ChangePassword(APIView):
    serializer_class = PasswordSerializer
    model = User
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk=None):
        serializer = PasswordSerializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.confirm_old_password(serializer):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        self.request.user.set_password(serializer.validated_data.get("new_password"))
        self.request.user.save()
        return Response({"detail": "Password successfully changed."})

    def confirm_old_password(self, serializer):
        old_password = serializer.validated_data.get("old_password")
        valid = self.request.user.check_password(old_password)
        if not valid:
            return False
        return True


class ForgotPasssword(APIView):
    permission_classes = []
    serializer_class = ForgotPasswordSerializer

    def get(self, request, format=None):
        raise MyCustomException("Method not allowed.", 405)

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)
        cls = list(User.objects.filter(id=user.id))
        if not len(cls) > 0:
            raise serializers.ValidationError("User with given email not found")
        reset_code = randint(111111, 999999)
        now = datetime.now().replace(tzinfo=utc)
        cls[0].time_code_created = now
        cls[0].reset_code = reset_code
        cls[0].save()
        name = user.first_name
        try:
            email_data = {"name": name, "reset_code": reset_code}
            email_send('Saringe Todo Reset Code', "forgot.html", email_data, [email, ])
            return Response({"detail": "Reset code sent successfully to {}.".format(email)})
        except Exception as e:
            print("The e is", e)
            return Response("Failed to send email!", status=status.HTTP_408_REQUEST_TIMEOUT)


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordserializer
    model = User
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(reset_code=serializer.validated_data.get("reset_code"))
        if not (datetime.now() <= user.time_code_created.replace(tzinfo=None) + timedelta(minutes=7)):
            raise serializers.ValidationError("The reset code has expired request another please!")
        user.set_password(serializer.data.get("new_password"))
        user.reset_code = None
        user.save()
        return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)


class RequestCodeApiView(APIView):
    model = User
    serializer_class = RequestCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = RequestCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        try:
            user = User.objects.get(username=username)
            name = user.first_name
            email = user.email
            reset_code = randint(111111, 999999)
            user.reset_code = reset_code
            user.time_code_created = datetime.now().replace(tzinfo=utc)
            user.save(update_fields=["reset_code", "time_code_created"])
            email_data = {"name": name, "reset_code": reset_code}
            email_send('Saringe Todo Reset Code', "forgot.html", email_data, [email, ])
            return Response("Code sent successfully to {}".format(email), status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        data = {}
        data["token"] = request.query_params.get("token")
        serializer = AccountVerifySerializer(data=data)
        valid = serializer.is_valid()
        failed_data = {'response': "Token expired . Try resending the verification email",
                       "heading": "Verification failed."}
        if not valid:
            return Response(failed_data, template_name='verify_account.html')
        token = serializer.validated_data.get("token")
        tokens = list(AccessToken.objects.filter(token=token))
        if len(tokens) != 1:
            return Response(failed_data,
                            template_name='verify_account.html')
        token = tokens[0]
        user = User.objects.filter(id=token.user_id)
        if len(user) != 1:
            return Response(failed_data,
                            template_name='verify_account.html')

        if user[0].verified:
            return Response({'response': "already active", "heading": "Already Verified"},
                            template_name='verify_account.html')
        user[0].verified = True
        user[0].save()
        return Response({'response': "now active", "heading": "Verified"}, template_name='verify_account.html')


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class RetrieveUpdateUserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"id": self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserProfileSerializer
        return UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer_used = self.get_serializer_class()
        ser = serializer_used(data=request.data)
        ser.is_valid(raise_exception=True)
        User.objects.filter(id=self.request.user.id).update(**ser.validated_data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class UserUpdateProfilePicture(generics.UpdateAPIView):
    serializer_class = ProfilePhotoSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        file = self.request.data.get('profile_photo')
        serializer = ProfilePhotoSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=self.request.user.id)
        user.profile_photo = serializer.validated_data.get("profile_photo")
        user.save()
        return Response("Photo updated successfully")
