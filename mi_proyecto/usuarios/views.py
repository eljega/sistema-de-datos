# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages  


def login_view(request):
    if request.method == 'POST':
        # Lógica para manejar los datos del formulario de inicio de sesión
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirigir a la URL de 'dashboard'
        else:
            # Mensaje de error de inicio de sesión
            messages.error(request, 'Usuario o contraseña incorrectos')
            pass
    # Si no es POST, simplemente renderiza el formulario de inicio de sesión
    return render(request, 'usuarios/login.html')

def dashboard_view(request):
    # Asegúrate de que el usuario está autenticado para ver el dashboard
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir a la URL de inicio de sesión si no está autenticado
    return render(request, 'usuarios/dashboard.html')
