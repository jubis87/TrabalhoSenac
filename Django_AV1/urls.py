from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('login.urls', 'accounts'))),  # namespace 'accounts' para login
    path('', include('gerenciamento_pedidos.urls')),  # URLs do seu app de pedidos
]
