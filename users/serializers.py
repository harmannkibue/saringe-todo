from rest_framework import serializers
from users.models import User
from mylib.images import Base64ImageField


class CreateUserSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, write_only=True, required=True, allow_blank=False)
    phone_number = serializers.CharField(max_length=14, required=True, allow_blank=False)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    profile_photo = Base64ImageField(required=False, max_length=None, use_url=True)
    username = serializers.CharField(read_only=True)

    def validate_email(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError("User with given email already exist.")
        return attrs

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with that phone number already exist")
        else:
            value = value.strip('+')
            if value[0] == '0':
                value = "254" + value[1:]
            return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance

    def get_profile_photo(self, obj):
        self.request = self.context.get("request")
        if obj.profile_photo:
            if self.request.build_absolute_uri:
                return self.request.build_absolute_uri(obj.profile_photo.url)
        return None

    def get_phone_number(self, obj):
        if obj.phone[0] == '0':
            phone = '254' + obj.phone[1:]
            return phone
        return self.phone

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'phone_number',
                  'first_name', 'last_name', 'profile_photo')


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password")


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email must be provided.")
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with that email not found.")
        return value


class ResetPasswordserializer(serializers.Serializer):
    reset_code = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_reset_code(self, value):
        if not User.objects.filter(reset_code=value).exists():
            raise serializers.ValidationError("Reset code Invalid or Expired", )
        return value


class RequestCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True, required=True)

    class Meta:
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'reset_code', 'groups', 'user_permissions', 'is_superuser',
                   'is_staff', 'time_code_created', 'modified')

    def get_name(self, obj):
        return obj.first_name + " " + obj.last_name


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    profile_photo = Base64ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'profile_photo')

    def get_username(self, obj):
        return obj.username

    def get_last_name(self, obj):
        return obj.last_name

    def get_first_name(self, obj):
        return obj.first_name

    def get_email(self, obj):
        return obj.email

    def get_phone_number(self, obj):
        return obj.phone_number

    def get_profile_photo(self, obj):
        self.request = self.context.get("request")
        if obj.profile_photo:
            if self.request.build_absolute_uri:
                return self.request.build_absolute_uri(obj.profile_photo.url)
        return None


class ProfilePhotoSerializer(serializers.Serializer):
    profile_photo = Base64ImageField(required=False, max_length=None, use_url=True)

    def get_profile_photo(self, obj):
        self.request = self.context.get("request")
        if obj.profile_photo:
            if self.request.build_absolute_uri:
                return self.request.build_absolute_uri(obj.profile_photo.url)
        return None

    def create(self, validated_data):
        User.objects.update(**validated_data)

    def update(self, instance, validated_data):
        validated_data['profile_photo'] = instance.profile_photo
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    profile_photo = Base64ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_photo')


class AccountVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
