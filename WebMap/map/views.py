from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from .models import Student
from django.contrib import messages
from django.contrib.auth.hashers import check_password


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

        try:
            student = Student.objects.get(username=username)

            # If password is stored in plaintext (not recommended for production):
            if student.password == password:
                request.session['student_id'] = student.id  # Optional: for session tracking
                return render(request, 'hello.html', {'student': student})

            # If using hashed passwords, use this instead:
            # if check_password(password, student.password):

            else:
                messages.error(request, "Invalid credentials")
                return render(request, 'login.html')

        except Student.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return render(request, 'login.html')

    return render(request, 'login.html')

def hello(request):
    return render(request, 'hello.html')

def signup(request):
    return render(request, 'signup.html')

def success (request):
    return render(request, 'success.html')

def login_check(request):
    username = request.session.get('login_username')
    password = request.session.get('login_password')

    if not username or not password:
        return JsonResponse({'error': 'Session expired or missing data'}, status=400)

    try:
        student = Student.objects.get(username=username)
        if check_password(password, student.password):
            return render(request, 'hello.html', {'student': student})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    except Student.DoesNotExist:
        return render(request, 'login.html', {'error': 'Invalid credentials'})
