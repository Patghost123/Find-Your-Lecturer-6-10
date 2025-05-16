from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .models import Student, Lecturer
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import requests

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
    
def floor_map(request, floor_number=1):
    if floor_number not in [1, 2, 3]:
        return render(request, '404.html', status=404)

    # Only include lecturers with non-empty room_number
    lecturers = Lecturer.objects.all() 

    lecturer_data = {
        lecturer.room_number.strip().upper(): {
            'name': lecturer.name,
            'room_number': lecturer.room_number,
            'position': lecturer.position,
            'email': lecturer.email,
            'phone': lecturer.phone,
            'faculty': lecturer.faculty,
            'profile_url': lecturer.profile_url,
        }
        for lecturer in lecturers
    }

    return render(request, f'floor{floor_number}map.html', {
        'floor': floor_number,
        'map_lecturer': lecturer_data,
    })
    
def home(request):
    lecturers = Lecturer.objects.all()  # Fetch all users from the database
    return render(request, "home.html", {"lecturers": lecturers})

def get_lecturers(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
    query = request.GET.get("q", "").strip().lower()
    if not isinstance(query, str):
        return JsonResponse({"error": "Invalid query parameter"}, status=400)
    if len(query) > 100:  
        return JsonResponse({"error": "Query too long"}, status=400)
    lecturers = Lecturer.objects.filter(name__icontains=query) if query else Lecturer.objects.all()

    return JsonResponse({
    "lecturers": list(lecturers.values("name", "slug"))
    })

def lecturer_profile(request, slug):
    lecturer = get_object_or_404(Lecturer, slug=slug)
    return render(request, "lecturer_profile.html", {"lecturer": lecturer})