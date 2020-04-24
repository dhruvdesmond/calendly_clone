from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404
import json
import requests

from .models import User,Meal
# Create your views here.


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


def search(food_name):
    # result = {}
    HEADERS = {"x-app-id": "732661df",
                "x-app-key":"80451c846f26dc21e903158a11fd29e9",
                "Content-Type": "application/json"
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    query = {"query": food_name}
    response = requests.post(url, headers=HEADERS, json=query)
    data = json.loads(response.content.decode("utf-8"))
    print(len(data['foods']))
    return (data['foods'][0]['nf_calories'])
def get_user(request, user_id):
    try:
        print(user_id)
        user = User.objects.get(pk=user_id)
        print(user.username)
    except User.DoesNotExist:
        raise Http404("User does not exit")
    meals = Meal.objects.filter(username=user.id)

    template = loader.get_template('calendly/user_detail.html')
    return HttpResponse(template.render({'user': user,'meals':meals}, request))


def edit_user(request, user_id):
    if request.method == "POST":
        data = request.POST

        password = data["password"]
        curr_calories = data["curr_calories"]
        totalCalories = data["total_calories"]
        User.objects.filter(pk=user_id).update(
            password=password, curr_calories=curr_calories, total_calories=totalCalories)
        User().save()
        return redirect("get_user", user_id)
    else:
        try:
            print(user_id)
            name = User.objects.get(pk=user_id)
            print(name.username)
        except User.DoesNotExist:
            raise Http404("User does not exit")
        template = loader.get_template('calendly/edit_user.html')
        return HttpResponse(template.render({'user': name}, request))


def get_all_users(request):
    try:
        list_of_users = User.objects.all()
    except User.DoesNotExist:
        raise Http404("User does not exit")
    template = loader.get_template('calendly/display_all_users.html')

    return HttpResponse(template.render({'list_of_users': list_of_users}, request))


def add_user(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        userName = data["user_name"]
        passWord = data["password"]
        totalCalories = data["total_calories"]
        User.objects.create(username=userName, password=passWord, curr_calories=0,
                            total_calories=totalCalories, calories_exceeded=False)
        User().save()
        return redirect('/users/')
    else:
        template = "calendly/signup.html"
        return render(request, template)

def add_meal(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        meal_name = data["meal_name"]
        calories = data["calories"]
        user_name = data["user_name"]
        get_user = User.objects.filter(username=user_name).first()
        if not get_user:
            return HttpResponse("Wrong user name")
        if calories:
            pass
        else:
            calories = search(meal_name)
        curr_calories = get_user.curr_calories + int(calories)
        if curr_calories >= get_user.total_calories:
            return HttpResponse("Calories exceeded for =",get_user.id)
        User.objects.filter(pk=get_user.id).update(curr_calories=curr_calories)
        Meal.objects.create(meal_name=meal_name, calories=calories, username=get_user)

        
        return redirect('/meals')
    else:
        template = "calendly/add_meal.html"
        return render(request, template)


def get_meal_by_id(request,meal_id):
    try:
        print(meal_id)
        name = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        raise Http404("Meal does not exit")
    template = loader.get_template('calendly/meal_detail.html')
    return HttpResponse(template.render({'meal': name}, request))

def get_meals(request):
    try:
        list_of_meals = Meal.objects.all()
    except Meal.DoesNotExist:
        raise Http404("Meals does not exit")
    template = loader.get_template('calendly/display_all_meals.html')
    return HttpResponse(template.render({'list_of_meals': list_of_meals}, request))

def result(request, user_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % user_id)
