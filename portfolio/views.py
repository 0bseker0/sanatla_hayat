from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    projects = Project.objects.all()
    return render(request,'portfolio/home.html', {'projects':projects})

def home_todo(request):
    return render(request,'portfolio/home_todo.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'portfolio/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'portfolio/signupuser.html',{'form':UserCreationForm(),'error':'Thar username has already taken. Pleae choose a new user name'})
        else:
            return render(request, 'portfolio/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'portfolio/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:  
            return render(request, 'portfolio/loginuser.html', {'form':AuthenticationForm(), 'error':'Kullanıcı adı ve şifre eşleşmedi.'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'portfolio\createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'portfolio\createtodo.html', {'form':TodoForm(), 'error':'Yanlış veri girilmiş'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True )
    return render(request,'portfolio\currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'portfolio\completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request,'portfolio\\viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'portfolio\\viewtodo.html', {'todo':todo, 'form':form, 'error':'Yanlış bilgi'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':    
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':    
        todo.delete()
        return redirect('currenttodos')