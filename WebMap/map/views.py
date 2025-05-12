from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import Student, Room
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.http import Http404

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
    
    return redirect("/hello/")


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
        return redirect("hello")  # 🚀 Redirect after successful login

    print("Login failed!")  # Debugging output
    return render(request, "login.html", {"error": "Invalid username or password!"})


def hello(request):
    # Use 'request.user' to check if the user is authenticated
    return render(request, 'hello.html', {'student': request.user if request.user.is_authenticated else None})

def success(request):
    return render(request, 'success.html')

def room_detail(request, room_code):
    try:
        room = Room.objects.select_related('lecturer').get(code=room_code)
        data = {
            "code": room.code,
            "name": room.name,
            "x": room.x,
            "y": room.y,
            "floor": room.floor,
            "lecturer": {
                "name": room.lecturer.name,
                "position": room.lecturer.position,
                "room_number": room.lecturer.room_number,
                "phone_number": room.lecturer.phone_number,
                "email": room.lecturer.email,
                "profile_url": room.lecturer.profile_url,
                "office_hours": room.lecturer.office_hours,
            } if room.lecturer else None
        }
        return JsonResponse(data)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
    
def floor_map(request, floor_number=1):
    if floor_number not in range(1, 5):  # allow floors 1 to 4
        raise Http404("Floor not found")

    template_name = f'floor{floor_number}map.html'
    return render(request, template_name, {'floor': floor_number})