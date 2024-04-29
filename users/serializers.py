from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['email', 'password']


class SignupSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField()

    class Meta:
        model = models.CustomUser
        fields = ['email', 'user_type', 'gender','first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this email already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.pop('user_type', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        if user_type is not None and user_type not in ['Tutor', 'Tutee', 'Admin']:
            raise serializers.ValidationError({'status': False, 'message': 'user_type should be either Tutor or Tutee'})
        instance.user_type = user_type
        instance.save()
        return instance


class CustomTokenGeneratorSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _('invalid credentials')
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['gender'] = user.gender
        token['user_type'] = user.user_type
        return token


class UserSerializer(serializers.ModelSerializer):
    tutor = serializers.SerializerMethodField()
    tutee = serializers.SerializerMethodField()

    class Meta:
        model = models.CustomUser
        fields = ['id','first_name','last_name','user_type', 'email','gender','is_staff',
            'is_active', 'is_superuser', 'tutor', 'tutee']

    def get_tutor(self, obj):
        if obj.user_type == "Tutor":
            tutor = models.Tutor.objects.filter(user=obj).first()
            if tutor:
                return TutorSerializer(tutor).data
            return None
        return None

    def get_tutee(self, obj):
            if obj.user_type == "Tutee":
                tutee = models.Tutee.objects.filter(user=obj).first()
                if tutee:
                    return TuteeSerializer(tutee).data
                return None
            return None


class TutorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Tutor
        fields = ['user', 'meetings_created', 'hours_spent']

    def get_user(self, obj):
         user_serializer = SimplifiedUserSerializer(obj.user)
         return user_serializer.data


class SimplifiedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class SimplifiedTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = ['id', 'meetings_created', 'hours_spent']

class TuteeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Tutee
        fields = ["user", "tutee_performance", "meetings_attended", "hours_spent"]

    def get_user(self, obj):
        user_serializer = SimplifiedUserSerializer(obj.user)
        return user_serializer.data
