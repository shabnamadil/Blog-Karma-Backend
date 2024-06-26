from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from apps.users.tokens import account_activation_token
from apps.users.models import (
    Profile
)

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            'id',
            'image',
            'bio',
            'profession',
            'mobile_number'
        )


class UserListSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'user_full_name',
            'email',
            'user_profile',
            'date_joined'
        )

    def get_date_joined(self, obj):
        local_joined_time = timezone.localtime(obj.date_joined)
        return local_joined_time.strftime('%d/%m/%Y, %H:%M')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirm',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove password_confirm from validated_data
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Deactivate account until it is confirmed
        user.save()
        current_site = Site.objects.get_current()
        subject = 'Activate Your Karma Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return user


class UserUpdateDestroySerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'user_profile'
        )

    def update(self, instance, validated_data):
        # Extract the nested user_profile data
        user_profile_data = validated_data.pop('user_profile', None)
        
        # Update the user instance fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update the user_profile instance fields
        if user_profile_data:
            user_profile = instance.user_profile
            user_profile.image = user_profile_data.get('image', user_profile.image)
            user_profile.profession = user_profile_data.get('profession', user_profile.profession)
            user_profile.mobile_number = user_profile_data.get('mobile_number', user_profile.mobile_number)
            user_profile.save()

        return instance
    
    def validate(self, attrs):
        user_profile_data = attrs['user_profile']
        if user_profile_data['profession'] and len(user_profile_data['profession']) < 5:
            raise ValidationError('Profession must be at least 5 characters')
        if user_profile_data['mobile_number'] and not user_profile_data['mobile_number'].isdigit():
            raise ValidationError('Only numeric values are allowed.')
        if user_profile_data['mobile_number'] and len(user_profile_data['mobile_number']) < 10:
            raise ValidationError('Mobile number must be at least 10 characters')
        return super().validate(attrs)
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()