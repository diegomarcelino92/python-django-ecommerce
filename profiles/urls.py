from django.urls import path

from profiles.views import ProfileCreate, ProfileLogin, ProfileLogout

app_name = 'profiles'

urlpatterns = [
    path('', ProfileCreate.as_view(), name='create'),
    path('login/', ProfileLogin.as_view(), name='login'),
    path('logout/', ProfileLogout.as_view(), name='logout'),
]
