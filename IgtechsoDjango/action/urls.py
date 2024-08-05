from django.urls import path,include
from action.views import UserRegistrationView,UserLoginView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name="register"),
    path('login/', UserLoginView.as_view(),name="login"),

]
