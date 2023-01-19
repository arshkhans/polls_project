from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['POST'])
def updateVote(request: Request):
    data = request.data

    question = Question.objects.get(pk=data['question_id'])

    def checkVote():
        for c in question.choice_set.all():
            if request.user.username in c.voted_user:
                return c.getID()
        return False
    
    exixtingId = checkVote()
    if exixtingId:
        temp = Choice.objects.get(pk=exixtingId)
        temp.remove_voted_user(request.user.username)
        temp.save()

    choice = Choice.objects.get(pk=data['choice_id'])
    choice.votes += 1
    choice.set_voted_user(str(request.user))
    choice.save()
    return Response({"ok":"okokok"})

@api_view(['POST'])
def checkVoted(request: Request):
    data = request.data
    choice = Choice.objects.get(pk=data['choice_id'])

    if str(request.user) in choice.voted_user:
        voted = True
    else:
        voted = False
    
    return Response({"voted":voted})

def home(request):
    context = {
        "poll": Question.objects.all()
    }
    return render(request, 'home.html',context)

def viewProfile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/home")
    context = {
        "poll": Question.objects.filter(user=request.user)
    }
    return render(request, 'profile.html',context)

def createPoll(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/home")
    if Question.objects.filter(user=request.user).count() >= 5:
        messages.error(request, 'Cant create more then 5 polls!')
    else:
        if request.method == "POST":
            qform = QuestionForm(request.POST, instance=Question())
            cforms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0,4)]
            if qform.is_valid() and all([cf.is_valid() for cf in cforms]):
                new_poll = qform.save(commit=False)
                new_poll.pub_date = datetime.now().replace(microsecond=0)
                new_poll.user = request.POST['user']
                new_poll.save()
                for cf in cforms:
                    new_choice = cf.save(commit=False)
                    new_choice.question = new_poll
                    new_choice.save()
                messages.success(request, 'Poll Created!')

    qform = QuestionForm(instance=Question())
    cforms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(0,4)]
    context = {  
        'question_form': qform,
        'choice_forms': cforms
    }
    return render(request, 'createPoll.html', context)

def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.info(request, "Logged in successfully.")
            return redirect("/login")
        else:
            messages.error(request, 'Error')
    else:  
        form = UserCreationForm()  
    context = {  
        'form':form  
    }
    return render(request, 'register.html', context)

def loginUser(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context = {  
        'form':form  
    }
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect("/home")
