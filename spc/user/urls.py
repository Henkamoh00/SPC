from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profileUpdate, name='profileUpdate'),
    path('signup/', views.signup, name='signupForm'),
    path('login/', views.login_, name='loginForm'),
    path('logout/', views.logoutAction, name='logout'),
    path('concerns/', views.concernsForm, name='concernsForm'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.passwordChange, name='passwordChange'),
    path('password_reset/', views.passwordReset, name='passwordReset'),
    path('password_reset/<uidb64>/<token>/', views.passwordResetConfirm, name='passwordResetConfirm'),
]