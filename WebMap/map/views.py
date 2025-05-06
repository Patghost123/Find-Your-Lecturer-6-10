from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import Student
from django.contrib import messages

def join(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
        else:
            student = Student(username=username, email=email)
            student.set_password(password)  
            student.save()
            # Log the user in immediately after signup
            auth_login(request, student)
            return redirect('hello')  # Redirect to the 'hello' page instead of rendering 'hello.html'
        
    return render(request, 'join.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student = authenticate(request, username=username, password=password)
        if student is not None:
            auth_login(request, student)
            return redirect('hello')  # Redirect to the 'hello' page after login
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def hello(request):
    # Use 'request.user' to check if the user is authenticated
    return render(request, 'hello.html', {'student': request.user if request.user.is_authenticated else None})

def success(request):
    return render(request, 'success.html')