from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import User
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_user(request,user_id):
    try:
        print(user_id)
        name = User.objects.get(pk=user_id)
        print(name.username)
    except User.DoesNotExist:
        raise Http404("User does not exit")
    template = loader.get_template('calendly/index.html') 

    return HttpResponse(template.render({'user': name}, request))

def edit_user(request,user_id):
    if request.method == "POST":
        data = request.POST

        password = data["password"]
        curr_calories = data["curr_calories"]
        totalCalories = data["total_calories"]
        User.objects.filter(pk=user_id).update(password=password,curr_calories=curr_calories,total_calories=totalCalories)
        User().save()
        return redirect("get_user",user_id)
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
        User.objects.create(username=userName,password=passWord,curr_calories=0,total_calories=totalCalories,calories_exceeded=False)
        User().save()
        return redirect('/users/')
    else:
        template = "calendly/signup.html"
        return render(request,template) 


def result(request,user_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response %user_id)

