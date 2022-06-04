from django.urls import path

from .views import index, other_pages, profile, cart, CDLoginView, CDLogoutView, ChangeUserInfoView,\
    ChangePasswordView, RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, band_view, item_view

app_name = 'main'
urlpatterns = [
    path('band/<int:pk>/', band_view, name='band'),
    path('item/<int:pk>/', item_view, name='item'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/login/', CDLoginView.as_view(), name='login'),
    path('accounts/logout/', CDLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('accounts/cart/', cart, name='cart'),
    path('', index, name='index'),
    path('<str:page>/', other_pages, name='other'),
]