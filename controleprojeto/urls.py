from argparse import Namespace
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    # Serviços
    path('', include('servicos.urls'), name='index'),

    # User Mange
    path('accounts/', include('allauth.urls')),

    # Django Admin
    path('admin/', admin.site.urls),
]


# path('accounts/', include('accounts.urls')),
# #path('accounts/', include('django.contrib.auth.urls')),
# path('usuarios/', include('usuarios.urls')),