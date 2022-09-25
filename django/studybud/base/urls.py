from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name ='login_page'),
    path('logout/', views.logout_user, name = 'logout_user'),
    path('resister/', views.resister_user, name = 'resister_user'),
    path('user_profile/<str:pk>/', views.user_profile, name = 'user_profile'),
    path("", views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    path("room_form/", views.createroom, name = "room_form"),
    path("room_update/<str:pk>/", views.updateroom, name = "update_room"),
    path("room_delete/<str:pk>/", views.deleteroom, name = 'delete_room'),
    path("message_delete/<str:pk>/", views.deletemessage, name = 'delete_message'),
    path('user_setting/', views.usersetting, name= 'user_setting'),
    path('topics/', views.topics, name = 'topics'),
    path('activity/', views.activity, name = 'activity')
]