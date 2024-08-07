from django.urls import path,include
from action.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,UserSendRestLinkView, UserResetPasswordView,BooksAndBrochureView,BlogView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name="register"),
    path('login/', UserLoginView.as_view(),name="login"),
    path('profile/', UserProfileView.as_view(),name="profile"),
    path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('reset/',UserSendRestLinkView.as_view(),name="RestPassword"),  
    path('reset-password/<cid>/<token>/',UserResetPasswordView.as_view(),name="RestPasswordChange"),
    path('books/',BooksAndBrochureView.as_view(),name="BooksAndBrochureView"),
    path('blog/',BlogView.as_view(),name="Blog")

]
