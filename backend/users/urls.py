from django.urls import include, path
from .views import UserList
urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    #path(r'(users/?P<uid>[\w-]+)/$', UserList.as_view(),),
]
