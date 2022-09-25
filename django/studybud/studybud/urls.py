"""studybud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings
# http stands for Hypertext Transfer Protocol

# not a good practice to have every function in project/urls.py 
# a good practice should be throw httprequets to each app from this main project urls.py
# and functions are placed on that each app's views.py 

# def home(request):
#     # request includes informations like what kind of method is given(post, get),
#     # what kind of data is given in 
#     return HttpResponse('Home Page')

# def room(request):
#     return HttpResponse('room')

urlpatterns = [
    # path imported abobe from django.urls
    # it looks to link urls with functions or classes respectively
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # if url includes api, look up for routes from 'base.api.urls'
    path('api/', include('base.api.urls'))
    # path("", home),
    # path("room/", room),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
