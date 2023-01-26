from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        token['email'] = user.email
        # token['phone'] = user.details.phone
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError('username not alnum')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=68, min_length=6, required=True)
    new_password = serializers.CharField(max_length=68, min_length=6, required=True)
    retype_password = serializers.CharField(max_length=68, min_length=6, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'retype_password']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Your old password was entered incorrectly. Please enter it again.'))
        return value

    def validate(self, attrs):
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError(_('No difference between old and new passwords'))
        if attrs.get('new_password') != attrs.get('retype_password'):
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ResetPasswordSerializer(serializers.ModelSerializer):
    pass


class SetNewPasswordSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(source='get_full_name')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'gender',
            'phone_number',
            'country',
            'city',
            'top_seller'
        ]

        def get_first_name(self, obj):
            return obj.first_name.title()

        def get_last_name(self, obj):
            obj.last_name.title()

        def to_representation(self, instance):
            representation = super(UserSerializer, self).to_representation(instance)
            if instance.is_superuser:
                representation["admin"] = True
            return representation
