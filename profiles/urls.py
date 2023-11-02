from django.urls import path

from profiles.views import (ProfileCreate, ProfileLogin, ProfileLogout,
                            ProfileUpdate)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileCreate.as_view(), name='create'),
    path('update/', ProfileUpdate.as_view(), name='update'),
    path('login/', ProfileLogin.as_view(), name='login'),
    path('logout/', ProfileLogout.as_view(), name='logout'),
]
