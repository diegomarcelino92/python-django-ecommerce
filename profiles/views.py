from django.shortcuts import render
from django.views import View

from profiles.forms import ProfileAddressForm, ProfileForm, UserForm
from profiles.models import Profile, ProfileAddress


class ProfileCreate(View):
    template_name = 'profile_create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        user_form = None
        profile_form = None
        profile_address_form = None

        if self.request.user.is_authenticated:
            user = self.request.user
            profile = Profile.objects.filter(user=user).first()
            profile_address = ProfileAddress.objects.filter(profile=profile).first()

            user_form = UserForm(
                data=self.request.POST or None,
                user=self.request.user,
                instance=self.request.user)

            profile_form = ProfileForm(data=self.request.POST or None, instance=profile)
            profile_address_form = ProfileAddressForm(data=self.request.POST or None, instance=profile_address)
        else:
            user_form = UserForm(data=self.request.POST or None)
            profile_form = ProfileForm(data=self.request.POST or None)
            profile_address_form = ProfileAddressForm(data=self.request.POST or None)

        self.context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile_address_form': profile_address_form
        }
        self.view = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.view

    def post(self, *args, **kwargs):

        return self.view


class ProfileUpdate(View):
    pass


class ProfileLogin(View):
    pass


class ProfileLogout(View):
    pass
