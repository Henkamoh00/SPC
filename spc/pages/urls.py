from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('post/<int:id>/<str:title>/', views.post, name='post'),
    path('<int:id>/<str:path>/', views.deleteComment, name='deleteComment'),
    path('comment/<int:id>/', views.commentUpdate, name='commentUpdateForm'),
]