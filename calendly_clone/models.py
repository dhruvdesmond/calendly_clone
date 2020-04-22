from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    curr_calories = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=2000)
    calories_exceeded = models.BooleanField()

class Meal(models.Model):
    meal_name = models.CharField(max_length=200)
    calories = models.IntegerField(max_length=99999)
    username = models.ForeignKey(User, on_delete=models.CASCADE)