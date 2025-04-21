from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import user
from django.contrib import messages

def join(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        print(f"POST data: username={username}, email={email}, passwd={passwd}")  # Debug form data

        if user.objects.filter(email=email).exists():
            print("Email already registered.")
            messages.error(request, "This email is already registered.")
        else:
            new_user = user(username=username, email=email, passwd=passwd)
            new_user.save()
            print(f"New user saved: {new_user}")  # Debug new user object
            messages.success(request, "Registered successfully!")
            return render(request, 'join.html')

    print("Handling GET request.")  # Debug for GET or unsupported methods
    return render(request, 'join.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's authentication system to check credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Logged in successfully!")
            return redirect('/hello')  # Redirect to a dashboard or home page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'hello.html')  # Render the login page

def hello(request):
    return render(request, 'hello.html')

def login(request):
    return render(request, 'login.html')


    

