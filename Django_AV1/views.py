from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('listar_pedidos')  # Redireciona para a página de pedidos
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})
