from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail


User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required = True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return email
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user

class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists(): # существует, проверяет
            raise serializers.ValidationError('Пользователь найден')
        return attrs
    
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email не найден')
        return email
    
    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError('Не верный email или пароль')
        else:
            raise serializers.ValidationError('Email и пароль обязательны к заполнению')
        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Вы ввели не корректный пароль')
        return old_password
    
    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass1 = data.get('new_password')
        new_pass2 = data.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        if old_pass == new_pass1:
            raise serializers.ValidationError('Этот пароль использовался ранее')
        return data
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя нет')
        return email
    

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail('Восстановление пароля',f'Ваш код восстановления {user.activation_code}','test@gmail.com',[user.email])
    

class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4,required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        password1 = data.get('password')
        password2 = data.get('password_confirm')

        if not User.objects.filter(email=email,activation_code = code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        if password1 != password2:
            raise serializers.ValidationError('пароли не совпадают')
        return data
    
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'






