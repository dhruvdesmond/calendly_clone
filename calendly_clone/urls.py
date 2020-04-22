from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/',views.get_user,name ="get_user"),
    path('users/',views.get_all_users,name ="list_of_users"),
    path('signup',views.add_user,name ="add_user")
]