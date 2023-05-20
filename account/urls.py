from django.urls import path
from .views import RegistrationView, ActivationView,LoginView,LogoutView,ChangePasswordView,ForgotPasswordView,ForgotPasswordCompleteView,UserView
from django.views.decorators.cache import cache_page


urlpatterns =[
    path('registr/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),  # вызывает тот метод который соответствует запросу
    path('login/', cache_page(60 * 5)(LoginView.as_view())),
    path('logout/',LogoutView.as_view()),
    path('change_password/',cache_page(60 * 5)(ChangePasswordView.as_view())),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/',cache_page(60 * 5)(ForgotPasswordCompleteView.as_view())),
    path('users/',cache_page(60 * 5)(UserView.as_view()))

]