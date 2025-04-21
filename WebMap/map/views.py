from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Student
from django.contrib import messages

def join(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        print(f"POST data: username={username}, email={email}, passwd={passwd}")  # Debug form data

        if Student.objects.filter(email=email).exists():
            print("Email already registered.")
            messages.error(request, "This email is already registered.")
        else:
            new_user = Student(username=username, email=email, passwd=passwd)
            new_user.save()
            print(f"New user saved: {new_user}")  # Debug new user object
            return render(request, 'hello.html')

    print("Handling GET request.")  # Debug for GET or unsupported methods
    return render(request, 'join.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authentication system to check credentials
        try:
            user = Student.objects.get(username=username, password=password)
            request.session["user_id"] = user.id  # Store session manually
            request.session["username"] = user.username
            login(request, user)  # Log the user in
            return redirect("hello")
        except Student.DoesNotExist:
            print("Invalid login credentials.")  # Debug
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

def hello(request):
    return render(request, 'hello.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def success (request):
    return render(request, 'success.html')

