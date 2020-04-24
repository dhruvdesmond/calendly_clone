from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/',views.get_user,name ="get_user"),
    path('edit/<int:user_id>/',views.edit_user,name ="edit_user"),
    path('users/',views.get_all_users,name ="list_of_users"),
    path('signup/',views.add_user,name ="add_user"),
    path('meal/<int:meal_id>/',views.get_meal_by_id,name ="get_meal_by_id"),
    path('addmeal/',views.add_meal,name ="add_meal"),
    path('meals/',views.get_meals,name ="get_meals")
    
]