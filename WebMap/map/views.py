from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .models import Student, Lecturer
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

def join(request):
    if request.method != "POST":  
        return render(request, "join.html")  

    # Guard clause for missing input
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()

    if not username or not email or not password:
        return render(request, "join.html", {"error": "All fields are required!"})

    if Student.objects.filter(username=username).exists():
        return render(request, "join.html", {"error": "Username already taken."})

    # Main signup logic
    student = Student(username=username, email=email, password=make_password(password))
    student.save()
    
    return redirect("/login/")


def login(request):
    if request.method != "POST":
        return render(request, "login.html")  

    # Extract login credentials
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()
    
    user = authenticate(request, username=username, password=password)

    # Handle authentication result
    if user is not None:
        print("User authenticated:", user.username)  
        auth_login(request, user)  
        print("Redirecting now...")  
        return redirect("home")  

    print("Login failed!")
    return render(request, "login.html", {"error": "Invalid username or password!"})


def home(request):
    return render(request, 'home.html', {'student': request.user if request.user.is_authenticated else None})

def success(request):
    return render(request, 'success.html')

def students_list(request):
    students = Student.objects.all()
    students = Student.objects.exclude(username__in=["FCILecturer", "adminfindyourlecturer"]).exclude(email__in=["FCILecturer@gmail.com", "adminfindyourlecturer@gmail.com"])
    return render(request, "students.html", {"students": students})
    
def floor_map(request, floor_number=1):       # select floor number based on selected florr
    if floor_number not in [1, 2, 3]:
        return render(request, '404.html', status=404)

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

    return render(request, f'floor{floor_number}map.html', {      # load the floor with the needed lecturers
        'floor': floor_number,
        'map_lecturer': lecturer_data,
    })
    
def home(request):
    lecturers = Lecturer.objects.all()  
    return render(request, "home.html", {"lecturers": lecturers})

def get_lecturers(request):
    if request.method != "GET":              # Any other method other than GET then return error
        return JsonResponse({"error": "Invalid request method"}, status=405)
    query = request.GET.get("q", "").strip().lower()

    if not isinstance(query, str):           # If user tries to query without proper parameters(string) then reject request
        return JsonResponse({"error": "Invalid query parameter"}, status=400)
    
    if len(query) > 100:                     # If query length more than 100 then reject request
        return JsonResponse({"error": "Query too long"}, status=400)
    lecturers = Lecturer.objects.filter(name__icontains=query) if query else Lecturer.objects.all()

    return JsonResponse({
    "lecturers": list(lecturers.values("name", "slug"))
    })

def lecturer_profile(request, slug):
    lecturer = get_object_or_404(Lecturer, slug=slug)
    return render(request, "lecturer_profile.html", {"lecturer": lecturer})