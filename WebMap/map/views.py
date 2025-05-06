from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from .models import Student
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password

def join(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"POST data: username={username}, email={email}, password={password}")

        if Student.objects.filter(email=email).exists():
            print("Email already registered.")
            messages.error(request, "This email is already registered.")
        else:
            hashed_password = make_password(password)
            new_user = Student(username=username, email=email, password=hashed_password)
            new_user.save()
            print(f"New user saved: {new_user}")
            return render(request, 'hello.html', {'student': new_user})

    print("Handling GET request.")
    return render(request, 'join.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(username=username)

            if check_password(password, student.password):
                request.session['student_id'] = student.id
                return render(request, 'hello.html', {'student': student})

            else:
                messages.error(request, "Invalid credentials")
                return render(request, 'login.html')

        except Student.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return render(request, 'login.html')

    return render(request, 'login.html')

def hello(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')  # redirect to login if not logged in

    student = Student.objects.get(id=student_id)
    return render(request, 'hello.html', {'student': student})

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
