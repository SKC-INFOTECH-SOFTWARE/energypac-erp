from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'employee_code', 'email', 'first_name',
                  'last_name', 'full_name', 'phone', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'employee_code'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_code'] = serializers.CharField()
        self.fields.pop('username', None)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['employee_code'] = user.employee_code
        token['name'] = user.get_full_name()
        return token

    def validate(self, attrs):
        employee_code = attrs.get('employee_code')
        password = attrs.get('password')

        try:
            user = User.objects.get(employee_code=employee_code)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid employee code or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid employee code or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
