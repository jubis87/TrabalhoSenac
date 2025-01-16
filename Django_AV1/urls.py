from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('login.urls', 'accounts'))),  # Adicione o namespace aqui
    path('', include('gerenciamento_pedidos.urls')),
]
