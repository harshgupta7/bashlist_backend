"""bashlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from server.resources import UserRegister
from server.resources import TestAuth
from server.resources import GetAccountURL
from server.resources import GetList
from server.resources import NewCredsPoster
from server.resources import RequestPushBucketURL
from server.resources import PushBucketConfirmation
from server.resources import RequestPullBucketURL
from server.resources import RequestEncCreds
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import handler404, handler500


handler404 = 'server.views.handle_error'
handler500 = 'server.views.handle_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',csrf_exempt(UserRegister.as_view())),
    path('api/v01/checkcredentials',csrf_exempt(TestAuth.as_view())),
    path('api/v01/getaccounturl',csrf_exempt(GetAccountURL.as_view())),
    path('api/v01/bashlist',csrf_exempt(GetList.as_view())),
    path('api/v01/reqbushbucket',csrf_exempt(RequestPushBucketURL.as_view())),
    path('api/v01/pbc',csrf_exempt(PushBucketConfirmation.as_view())),
    path('api/v01/reqpull/<slug:bucket_name>',csrf_exempt(RequestPullBucketURL.as_view())),
    path('api/v01/getcreds',csrf_exempt(RequestEncCreds.as_view())),
    path('api/v01/postnewcreds',csrf_exempt(NewCredsPoster.as_view()))
]
