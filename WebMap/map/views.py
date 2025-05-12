from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import Student
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def join(request):
    if request.method != "POST":  # Guard clause for GET requests
        return render(request, "join.html")  

    # Guard clause for missing input
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()

    if not username or not email or not password:
        return render(request, "join.html", {"error": "All fields are required!"})

    if Student.objects.filter(username=username).exists():
        return render(request, "join.html", {"error": "Username already taken."})

    # Main logic
    student = Student(username=username, email=email, password=make_password(password))
    student.save()
    
    return redirect("/login/")


def login(request):
    # Guard clause: Immediately return the login page for GET requests
    if request.method != "POST":
        return render(request, "login.html")  

    # Extract login credentials
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    # Attempt authentication using Django's built-in `authenticate`
    user = authenticate(request, username=username, password=password)

    # Handle authentication result
    if user is not None:
        print("User authenticated:", user.username)  # Debugging output
        auth_login(request, user)  # Logs the user in
        print("Redirecting now...")  # Debugging output
        return redirect("home")  # Redirect after successful login

    print("Login failed!")  # Debugging output
    return render(request, "login.html", {"error": "Invalid username or password!"})


def home(request):
    return render(request, 'home.html', {'student': request.user if request.user.is_authenticated else None})

def success(request):
    return render(request, 'success.html')

def students_list(request):
    students = Student.objects.all()
    students = Student.objects.exclude(username__in=["FCILecturer", "adminfindyourlecturer"]).exclude(email__in=["FCILecturer@gmail.com", "adminfindyourlecturer@gmail.com"])
    return render(request, "students.html", {"students": students})