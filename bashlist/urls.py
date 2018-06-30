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
