from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Student
from django.contrib import messages

def join(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"POST data: username={username}, email={email}, password={password}")  # Debug form data

        if Student.objects.filter(email=email).exists():
            print("Email already registered.")
            messages.error(request, "This email is already registered.")
        else:
            new_user = Student(username=username, email=email, password=password)
            new_user.save()
            print(f"New user saved: {new_user}")  # Debug new user object
            return render(request, 'hello.html')

    print("Handling GET request.")  # Debug for GET or unsupported methods
    return render(request, 'join.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hello')  # or your homepage route
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

def hello(request):
    return render(request, 'hello.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def success (request):
    return render(request, 'success.html')

