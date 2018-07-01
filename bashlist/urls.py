from django.contrib import admin
from django.urls import path
from server.Resources.account import GetAccountURL
from server.Resources.delete import GetBucketInfo
from server.Resources.delete import DeleteBucketConf
from server.Resources.pull import RequestPullBucketURL
from server.Resources.push import RequestPushBucketURL
from server.Resources.push import PushBucketConfirmation
from server.Resources.list import GetList
from server.Resources.passchange import RequestEncCreds
from server.Resources.passchange import NewCredsPoster
from server.Resources.util import UserRegister
from server.Resources.util import TestAuth
from server.Resources.util import GetPublicKey
from server.Resources.share import ShareBucketRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import handler404, handler500

handler404 = 'server.views.handle_error'
handler500 = 'server.views.handle_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', csrf_exempt(UserRegister.as_view())),
    path('api/v01/checkcredentials', csrf_exempt(TestAuth.as_view())),
    path('api/v01/getaccounturl', csrf_exempt(GetAccountURL.as_view())),
    path('api/v01/bashlist', csrf_exempt(GetList.as_view())),
    path('api/v01/reqbushbucket', csrf_exempt(RequestPushBucketURL.as_view())),
    path('api/v01/pbc', csrf_exempt(PushBucketConfirmation.as_view())),
    path('api/v01/reqpull/<slug:bucket_name>', csrf_exempt(RequestPullBucketURL.as_view())),
    path('api/v01/getcreds', csrf_exempt(RequestEncCreds.as_view())),
    path('api/v01/postnewcreds', csrf_exempt(NewCredsPoster.as_view())),
    path('api/v01/gbi', csrf_exempt(GetBucketInfo.as_view()))
]
