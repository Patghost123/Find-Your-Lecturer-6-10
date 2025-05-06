from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        # Temporarily store in session
        request.session['login_username'] = username
        request.session['login_password'] = password

        return redirect('login_check')  # Redirect to GET check view

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def hello(request):
    return render(request, 'hello.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def success (request):
    return render(request, 'success.html')


def login_check(request):
    username = request.session.get('login_username')
    password = request.session.get('login_password')

    if not username or not password:
        return JsonResponse({'error': 'No login data found'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
